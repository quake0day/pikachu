# pikachu
Automatic grading script created by Si Chen



##How to use it (Timberlake)

1. Copy all students homework submissions to your Timberlake folder
2. Copy this repo to that folder 
	
		git clone 
		
	
5. Run (the) grading script

		python grading.py
		
6. The running result for each student will be in ./res folder


##How to use it (Local OSX)

1. Download all students homework submissions to a local folder 

		scp -r enshuwan@timberlake.cse.buffalo.edu:/submit/bina/CSE241/ ./
2. Copy grading script (grading.py) to that folder 
3. Install pick using pip
	
		sudo pip install pick

4. Install iverilog using Homebrew
	
		brew install icarus-verilog
	
5. Run (the) grading script

		python grading.py
		
6. The running result for each student will be in ./res folder
