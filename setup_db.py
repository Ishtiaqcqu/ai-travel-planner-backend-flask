import os
import logging
import argparse
from app import create_app
from app.utils.db_utils import (
    init_migrations,
    create_migration,
    upgrade_database,
    list_tables
)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def setup_database():
    """Complete database setup process."""
    app = create_app()
    
    # List tables before migration
    tables_before = list_tables(app)
    
    # Run migration steps
    migration_steps = [
        ("Initialize migrations", init_migrations),
        ("Create migration", create_migration),
        ("Upgrade database", upgrade_database)
    ]
    
    for step_name, step_func in migration_steps:
        logger.info(f"Running step: {step_name}")
        success = step_func()
        if not success:
            logger.error(f"Step failed: {step_name}")
            return False
        logger.info(f"Step completed: {step_name}")
    
    # List tables after migration
    tables_after = list_tables(app)
    
    # Check if users table was created
    if 'users' in tables_after and 'users' not in tables_before:
        logger.info("Users table was successfully created")
    elif 'users' in tables_after:
        logger.info("Users table already exists")
    else:
        logger.error("Users table was not created!")
        return False
    
    logger.info("Database setup completed successfully")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Database setup tool")
    parser.add_argument('--action', choices=['setup', 'init', 'migrate', 'upgrade', 'list-tables'],
                        default='setup', help='Action to perform')
    
    args = parser.parse_args()
    app = create_app()
    
    if args.action == 'setup':
        setup_database()
    elif args.action == 'init':
        init_migrations()
    elif args.action == 'migrate':
        create_migration()
    elif args.action == 'upgrade':
        upgrade_database()
    elif args.action == 'list-tables':
        list_tables(app) 