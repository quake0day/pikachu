# pikachu

Automatic grading script created by Si Chen



##How to use it (Timberlake)

1. Clone this repo to your home folder 
	
		git clone https://github.com/quake0day/pikachu.git
		
		cd pikachu

2. Copy all students homework submissions to that folder
		
		cp -r /submit/bina/CSE241/* ./
	
	
3. Run (the) grading script

		python2 grading.py
		
4. The running result for each student will be stored in ./res folder


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
