#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <stdlib.h>
#include <algorithm>
#include <stdio.h>
#include <string.h>

using namespace std;

int iterations=0;
//this is really similar to calculating 
//the levenshtein distance
//using the Wagner-Fischer algo
int LevDist(string s, string t, int len_s, int len_t) { 

//initializing matrix 
//int D[len_s][len_t];

// int (*D)[len_t] = malloc(sizeof *D * len_s);
int *D = malloc( sizeof(int) * (len_s + 1) * (len_t + 1));
memset(D, '\0', sizeof(D));


//distance to empty string 
for (int i = 0;i<len_s;i++)
	D[i * len_t + 0] = i; 

for (int j = 0;j<len_t;j++)
	D[0 * len_t + j] = j; 

//use dynamic programming
//DP[i,j] = the min number of operations (modified edit distance) 
//to transform from substack(s, 0, i)
//to substack(t, 0, j)
for (int i=1; i<len_s+1; i++) 
	for(int j=1; j<len_t+1; j++) { 
		iterations++;
		// uncomment to show steps
		cout << "s sub: " << s.substr(0,i) << endl << "t sub: "<< t.substr(0,j) << endl;
		if (s.substr(i-1,1) == t.substr(j-1,1)) {//string index starts at zero. D[0,0] for empty strings
			D[i * len_t + j] = D[(i-1) * len_t + j-1];
			// uncomment to show steps
			cout << "i,j = " << i << "," << j << endl;
			cout << s.substr(i-1,1) << "==" << t.substr(j-1,1) << endl << "D[i][j]: " << D[i * len_t + j] << endl;
			cout << "--------" << iterations << endl;
		} else { 
			if (i <= j) {
				if (i == len_s){
				D[i * len_t + j] = min(
					//then we have the option of 
					//adding a box at the top of s
				 	D[i * len_t + j-1] + 1, 
				 	// min(
				 		//deleting this box from s
				 		// D[(i-1) * len_t + j ]+ 1,
				 		//substitute a box
						D[(i-1) * len_t + j-1] + 1);
				} else {
					D[i * len_t + j] = D[(i-1) * len_t + j-1] + 1;
				} 
			} else {
				if (i == len_s){
					D[i * len_t + j] = min( 
					D[i * len_t + j-1] + 1, min(
					D[(i-1) * len_t + j] + 1,
					D[(i-1) * len_t + j-1] + 1));
				} else {
					D[i * len_t + j] = min(
					 //deleting a box anywhere from s
					 D[(i-1) * len_t + j] + 1, 
					 //substitute a box
					 D[(i-1) * len_t + j-1] + 1);
				}
			}
				// uncomment to show steps 
cout << "D[i][j]: " << D[i * len_t + j] << endl;
cout << "--------" << iterations << endl;

		}
	};

	free(D);
	int d =D[len_s * len_t + len_t]; 
//return the min operation to get from s to t   
return d;
}


int main(int argc, char ** argv)
{
	if (argc == 2) {
		clock_t start, stop;
		start = clock();

		std::ifstream file(argv[1]);
		int sum = 0;
		int levDist, rno, cno, lineno=0;
		//initialize a vector of strings
		//strings[0] to strings[cno-1] are "s" strings
		//strings[cno] to strings[2cno-1] are the corresponding "t" strings
		std::vector<string> strings;
		for(std::string line; getline(file, line); ) {
			if (line.substr(0,1) != "#"){ //assume no evil spaces
				lineno++;
				if (lineno == 1) {
						rno = atoi(line.c_str());
				} else if (lineno == 2) { 
						cno = atoi(line.c_str());
						for (int c=0; c<cno * 2; c++)
							strings.push_back("");
				} else {//if no evil test cases
						//rno and cno should be nonzero
						//append this char to start of string if it's not "-"		
						for(int c=0; c<cno; c++)
							if (line.substr(2*c,1) != "-")
								strings[c + ((int)(lineno-2)/(rno+1)) * cno].insert(0, line.substr(2*c,1));
				}
			}
		}

		for (int i=0; i<cno; i++){

			std::string s = strings[i];
			std::string t = strings[i + cno];
			// uncomment below to see steps
			cout << "string s: " << s << endl;
			cout << "string t: " << t << endl;
			levDist = LevDist(s, t, s.size(), t.size());
			sum += levDist;
			// uncomment below to see steps
			cout << "LevDist: " << levDist << endl << endl;
		}

		cout << sum << endl;
		stop = clock();
		double timeTaken = (double) (stop - start)/ CLOCKS_PER_SEC;
		cout << "Time taken: " << timeTaken << "sec" << endl;

	} else {
		cout << "usage: " << argv[0] << " <input file>" << endl;
	}
}