from def_shed import create_app
# from waitress import serve       # waitress server 

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)  # development server
    # serve(app, host='0.0.0.0', port=5000)           # waitress server 
