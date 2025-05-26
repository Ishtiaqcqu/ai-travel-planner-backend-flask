from flask import request, g
from app.models import db
from app.models.api_hit import ApiHit
import time
from functools import wraps

def track_api_hit(f):
    """Decorator to track API endpoint hits"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        
        # Get request information
        endpoint = request.endpoint or request.path
        method = request.method
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent', '')
        user_id = getattr(g, 'user_id', None)  # Assuming user_id is stored in g
        
        try:
            # Execute the original function
            response = f(*args, **kwargs)
            
            # Calculate response time
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            # Get status code
            status_code = getattr(response, 'status_code', 200)
            
            # Create API hit record
            api_hit = ApiHit(
                endpoint=endpoint,
                method=method,
                user_id=user_id,
                ip_address=ip_address,
                user_agent=user_agent,
                status_code=status_code,
                response_time=response_time
            )
            
            db.session.add(api_hit)
            db.session.commit()
            
            return response
            
        except Exception as e:
            # Calculate response time even for errors
            response_time = (time.time() - start_time) * 1000
            
            # Create API hit record for error
            api_hit = ApiHit(
                endpoint=endpoint,
                method=method,
                user_id=user_id,
                ip_address=ip_address,
                user_agent=user_agent,
                status_code=500,
                response_time=response_time
            )
            
            try:
                db.session.add(api_hit)
                db.session.commit()
            except:
                # If we can't save the hit, don't break the original request
                pass
            
            # Re-raise the original exception
            raise e
    
    return decorated_function

def get_api_stats():
    """Get API statistics for the admin dashboard"""
    from sqlalchemy import func
    
    # Get hit count by endpoint
    endpoint_stats = db.session.query(
        ApiHit.endpoint,
        ApiHit.method,
        func.count(ApiHit.id).label('hit_count'),
        func.avg(ApiHit.response_time).label('avg_response_time')
    ).group_by(ApiHit.endpoint, ApiHit.method).all()
    
    # Get total hits
    total_hits = db.session.query(func.count(ApiHit.id)).scalar()
    
    # Get hits by status code
    status_stats = db.session.query(
        ApiHit.status_code,
        func.count(ApiHit.id).label('count')
    ).group_by(ApiHit.status_code).all()
    
    return {
        'endpoint_stats': [
            {
                'endpoint': stat.endpoint,
                'method': stat.method,
                'hit_count': stat.hit_count,
                'avg_response_time': round(stat.avg_response_time, 2) if stat.avg_response_time else 0
            }
            for stat in endpoint_stats
        ],
        'total_hits': total_hits,
        'status_stats': [
            {
                'status_code': stat.status_code,
                'count': stat.count
            }
            for stat in status_stats
        ]
    } 