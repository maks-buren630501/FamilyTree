import sys

from core.database.migrations import make_migrations, migrate, downgrade

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('need command')
    command = sys.argv[1]
    if command == 'make':
        make_migrations()
    elif command == 'migrate':
        migrate()
    elif command == 'downgrade':
        revision = sys.argv[2] if len(sys.argv) == 3 else '-1'
        downgrade(revision)
    else:
        print('unknown command')


