from my_project import db


# M:M relationships
class CompositorAlbum(db.Model):
    __tablename__ = 'compositor_album'

    compositor_id = db.Column(db.Integer, db.ForeignKey('compositor.id'), primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), primary_key=True)
