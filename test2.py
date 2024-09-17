import time
import logging
import random

# Banner
BANNER = """
  ______   __                            __      _______                        
 /      \ /  |                          /  |    /       \                       
/$$$$$$  |$$ |____    ______    _______  $$ |   /$$$$$$$  |  ______    _______   
$$ |  $$/ $$      \  /      \  /       \ $$ |   $$ |__$$ | /      \  /       \  
$$ |      $$$$$$$  | $$$$$$  |/$$$$$$$/ $$ |   $$    $$<  $$$$$$  |/$$$$$$$/   
$$ |   __ $$ |  $$ | /    $$ |$$ |      $$ |   $$$$$$$  | /    $$ |$$ |          
$$ \__/  |$$ |  $$ |/$$$$$$$ |$$ \_____ $$ |   $$ |  $$ |/$$$$$$$ |$$ \_____     
$$    $$/ $$ |  $$ |$$    $$ |$$       |$$ |   $$ |  $$ |$$    $$ |$$       |    
 $$$$$$/  $$/   $$/  $$$$$$$/  $$$$$$$/ $$/    $$/   $$/  $$$$$$$/  $$$$$$$/     

"""

# Set up logging with custom colors: timestamp in gray, log message in green, additional info in white
logging.basicConfig(
    level=logging.INFO,
    format="\033[90m%(asctime)s\033[0m \033[92m%(message)s\033[0m",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Tap handling class with session and timing logic
class TapHandler:
    def __init__(self, max_tap=3000):
        self.max_tap = max_tap
        self.current_tap = 0
        self.session_start_time = time.time()
        self.total_time = 0

    def tap(self):
        if self.current_tap < self.max_tap:
            increment = random.randint(55, 60)  # Randomized increment between 55 and 60
            self.current_tap += increment
            if self.current_tap > self.max_tap:
                self.current_tap = self.max_tap  # Ensure it doesn't exceed max tap
            logging.info(f"Current Tap: {self.current_tap}")
        else:
            logging.info("Max tap reached")

    def check_time(self):
        session_duration = time.time() - self.session_start_time
        logging.info(f"Session Duration: {session_duration:.2f} seconds")
        self.total_time += session_duration
        return session_duration

    def reset(self):
        self.current_tap = 0
        self.session_start_time = time.time()
        logging.info("Tap count reset for a new session")

# Simulated logic, can replace this with your custom logic (including tapping and other tasks)
class Simulation:
    def __init__(self, max_tap):
        self.tap_handler = TapHandler(max_tap)

    def run(self):
        while self.tap_handler.current_tap < self.tap_handler.max_tap:
            self.tap_handler.tap()
            time.sleep(random.uniform(0.1, 0.5))  # Simulate waiting period between taps

        session_time = self.tap_handler.check_time()
        if session_time > 10:  # Example session timing logic
            self.tap_handler.reset()

# Running the simulation with banner
def main():
    print(BANNER)
    max_tap = 3000
    sim = Simulation(max_tap)
    
    for session in range(3):  # Example of running multiple sessions
        logging.info(f"Starting session {session + 1}")
        sim.run()
        logging.info(f"Session {session + 1} completed")

if __name__ == "__main__":
    main()

