def get_or_create(sql_session, model, **kwargs):
    """
        Самописный get_or_create, потому что почему-то его нет в алхимии
    """
    instance = sql_session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        sql_session.add(instance)
        sql_session.commit()
        return instance
