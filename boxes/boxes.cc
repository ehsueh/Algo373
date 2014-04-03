#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <stdlib.h>
#include <algorithm>

using namespace std;

//this is really similar to calculating 
//the levenshtein distance
//using the Wagner-Fischer algo
int LevDist(string s, string t, int len_s, int len_t) { 

//initializing matrix 
int D[len_s][len_t];

//distance to empty string 
for (int i = 0;i<len_s;i++)
	D[i][0] = i; 

for (int j = 0;j<len_t;j++)
	D[0][j] = j; 

//use dynamic programming
//DP[i,j] = the min number of operations (modified edit distance) 
//to transform from substack(s, 0, i)
//to substack(t, 0, j)
for (int i=1; i<len_s+1; i++) 
	for(int j=1; j<len_t+1; j++) { 
		// uncomment to show steps
		// cout << "s sub: " << s.substr(0,i) << endl << "t sub: "<< t.substr(0,j) << endl;
		if (s.substr(i-1,1) == t.substr(j-1,1)) { //string indexing starts at zero
			D[i][j] = D[i-1][j-1];
			// uncomment to show steps
			// cout << "i,j = " << i << "," << j << endl;
			// cout << s.substr(i,1) << "==" << t.substr(j,1) << endl << D[i][j] << endl;
		} else { 
			if (i==len_s) {
				D[i][j] = min(
					//adding a box at the top of s
				 	D[i][j-1]+1, 
				 	min(
				 		//deleting this box from s
				 		D[i-1][j]+1,
				 		//substitute a box
						D[i-1][j-1] + 1)); 
				// uncomment to show steps 
				// cout << "D[i][j]: " << D[i][j] << endl;
			} else {
				D[i][j] = min(
					 //deleting a box anywhere from s
					 D[i-1][j]+1, 
					 //substitute a box
					 D[i-1][j-1] + 1);
				// uncomment to show steps 
				// cout << "D[i][j]: " << D[i][j] << endl;
			}
		}
	};
//return the min operation to get from s to t 
return D[len_s][len_t];
}


int main(int argc, char ** argv)
{
	if (argc == 2) {
		std::ifstream file(argv[1]);
		int sum = 0;
		int rno, cno, lineno=0;
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
			// cout << "string s: " << s << endl;
			// cout << "string t: " << t << endl;
			sum += LevDist(s, t, s.size(), t.size());
			// uncomment below to see steps
			// cout << "LevDist: " << LevDist(s, t, s.size(), t.size()) << endl << endl;
		}

		cout << sum << endl;

	} else {
		cout << "usage: " << argv[0] << " <input file>" << endl;
	}
}