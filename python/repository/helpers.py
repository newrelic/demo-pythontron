def inventory_repository_selector(app_config = None):
    if app_config == None:
        from dependency_injection_container import Container
        app_config = Container().app_config()
    
    database_options = app_config.get_app_config_value('database')
    option_values = [database_options.get(i, '') for i in ['user', 'password', 'host', 'port', 'database']]

    # false if there exists an option with no value, true if all options have values
    use_database = not('' in option_values)

    selection = "database" if use_database else "file"

    print(f"Using inventory repository type: {selection}")

    return selection
