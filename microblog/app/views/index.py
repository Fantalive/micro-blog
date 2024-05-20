from flask import Blueprint, render_template

main_bp = Blueprint( 'main', __name__ )

@main_bp.route( '/' )
def index():
	# add any other necessary data fetching logic here.
	return render_template( 'index.html' )