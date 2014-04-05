#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <stdlib.h>
#include <algorithm>
#include <stdio.h>
#include <string.h>
#include <sstream> //for isstringstream

using namespace std;

int main(int argc, char ** argv)
{
	if (argc == 2) {
		clock_t start, stop;
		start = clock();

		std::ifstream file(argv[1]);
		std::vector<double> w;

		int n, m, lineno=0;
		double cost;

		for(std::string line; getline(file, line);){
			if (line.substr(0,1) != "#"){ // assume no evil spaces
				lineno++;
				if (lineno == 1) {
					// number of services in S
					n = atoi(line.c_str());
				} else if (lineno == 2) { 


					// number of companies in C
					m = atoi(line.c_str());
				} else if (lineno >= 3 && lineno <= n + 3) {
					// put real numbers w_i (cost of not
					// obtaining any company with service i	
					// into vector of doubles, call it w
					w.push_back(atoi(line.c_str()));
				} else {
					// calculate/ approximate answer using these final m lines
					// first double will be cost of companies
					// the rest of the integers will be the services it has
					
					int *D = malloc(sizeof(double) * (m+1) * (n+1));
					memset(D, '\0', sizeof(D));

					// std::vector<double> D (m*n + m, 0.0);
					std::vector<int> occur (n, 0);
					// this will store only the company cost of the first occurence of a service
					std::vector<double> S2C (n, 0);

					std::istringstream iss(line);
					string entry;
					int term = 1;
					while (iss >> entry){
						if (term == 1){
							// associate cost of company to company id
							// D[i * colno] = cost of company i 
							//insert into the pseudo m*n+1 matrix
							D[(lineno - n - 4) * (n + 1)] = (double) atoi(entry.c_str());
						} else {
							// occur[i] = number of occurrence of this service
							occur[atoi(entry.c_str())]++;
							// add this value to corresponding company
							D[(lineno - n - 4) * (n + 1) + term - 1] = (double) atoi(entry.c_str());
						}
						term++;
					}
					// int colno = n + 1;
					// int rowno = m;
					// D[i * (n+1) + n] is the
					// number of services company i covers
					D[(lineno - n - 4) * (n + 1)] = (double) term;

					// loop through occur once
					
					// if exactly one company (c) has it, take min of w(s) and cost(c)
					for (int i=0; i<n; i++)
						if (occur[i] == 0) {// if zero companies offers service s, add w(s)
							cost += w[i];
						} else if (occur[i] == 1) {
							// look up price of this service?
							cost += min(w[i], S2C[i]);
						};

					// now the complicated part
					// for an approximation.... 
					// take the min of the following
					// note this is not covering all the possible costs
					// we're going by an optimizer's mindset: avoiding worst case
					// and hopefully hitting the best case some of the times	
					// e.g. greedily choose the companies with the most service
                                        // some score c/#service 
                                        // network flow? Or LP, IP? 
					// cost += min()
					free(D);	
				}


			
			}
		}




		cout << cost << endl;
		stop = clock();
		double timeTaken = (double) (stop - start)/ CLOCKS_PER_SEC;
		cout << "Time taken: " << timeTaken << "sec" << endl;

	} else {
		cout << "usage: " << argv[0] << " <input file>" << endl;
	}

}
