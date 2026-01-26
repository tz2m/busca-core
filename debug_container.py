import os
import sys

# Add src to path
sys.path.append(os.path.abspath("src"))

from busca.app.container import Container


def check_container():
    container = Container()
    
    # Mock config
    container.config.nota_ri.database.user.from_value("user")
    container.config.nota_ri.database.password.from_value("pass")
    container.config.nota_ri.database.host.from_value("localhost")
    container.config.nota_ri.database.port.from_value(5432)
    container.config.nota_ri.database.db_name.from_value("db")

    print(f"Checking session_factory_nota_ri...")
    factory = container.session_factory_nota_ri()
    print(f"session_factory_nota_ri type: {type(factory)}")
    print(f"Is factory callable? {callable(factory)}")

    print(f"Checking session_nota_ri...")
    session_obj = container.session_nota_ri()
    print(f"session_nota_ri type: {type(session_obj)}")
    
    if hasattr(session_obj, 'query'):
        print("session_obj has .query() method")
    else:
        print("session_obj DOES NOT have .query() method")

    # Check repository injection
    print(f"Checking repo...")
    repo = container.nota_ri_repo_sql()
    print(f"Repo session type: {type(repo.session)}")

if __name__ == "__main__":
    check_container()
