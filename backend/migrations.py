import sys

from core.database.migrations import make_migrations, migrate

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('need command')
    command = sys.argv[1]
    if command == 'make':
        make_migrations()
    elif command == 'migrate':
        migrate()
    else:
        print('unknown command')


