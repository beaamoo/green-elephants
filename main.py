from src.app import app
import subprocess

if __name__ == '__main__':
  # Define a list of users to send messages to
  subprocess.run(['python', '/Users/adnanbhanji/Documents/GitHub/green-elephants/starter.py'])
  app.run(host='0.0.0.0', port=8000, debug=True,  use_reloader=False)