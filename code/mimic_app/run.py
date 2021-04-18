from web_application import app
import sys

if __name__ == '__main__':
    # p = int(sys.argv[1])
    app.run(host='0.0.0.0', port=5005, threaded=True, debug=False)
