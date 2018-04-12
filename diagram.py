from eralchemy import render_er
import models

if __name__ == '__main__':
    """
    Creates ER Diagram
    
    Library: https://github.com/Alexis-benoist/eralchemy
    """
    render_er(models.db.make_declarative_base(models.db.metadata), 'documents/models.png')