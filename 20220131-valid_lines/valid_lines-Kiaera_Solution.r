############################################
## Why Dox, why?
############################################

#MxN grid
#C collinear centers

WhyDox <- function(M,N,C){

if(C==1 || C==2 || C > max(M,N)){
	print("I hate you")
	opt <- options(show.error.messages = FALSE)
	stop()
}

#this will be easier if I know that M >= N, so let's just do that
if(N > M){
	M1 <- M
	M <- N
	N <- M1
}

############################################
## Horizontal and Vertical
############################################

#M lines of length N and N lines of length M

horizontal <- M*choose(N,C)
vertical <- N*choose(M,C)

############################################
## Diagonal
############################################

#big diagonals
diagonal <- 2*(1+M-N)*choose(N,C)

#4 of length (N-1), (N-2), etc out to length C if
if(min(M,N) > C){
	for(i in (N-1):C){
		diagonal <- diagonal + 4*choose(i,C)
	}
}
############################################
## Bricks
############################################

#initialize some empty data frames
bricks <- data.frame()
bricksnew <- data.frame()
brickstotal <- data.frame()

#looping through bricks of various ixj sizes
for (i in 1:((M-1)/(C-1))){
	for (j in 1:((N-1)/(C-1))){
		#taking care of the 2-1 and 4-2 type duplicate problem
		tagsall <- TRUE
		for (dup in 2:((M-1)/(C-1))){
			tagsall[dup-1] <- i%%dup == 0 && j%%dup == 0
			tag <- as.logical(sum(tagsall))
		}
		if(!tag && i!=j){
			#k is number of "centers" in a line
			for (k in M:C){
				#don't count bricks that can't happen
				if((M-i*(k-1)) > 0 && (N-j*(k-1)) > 0){
					#Number of lines that fit brick with k centers
					length <- (M-i*(k-1))*(N-j*(k-1)) 
					bricksnew <- data.frame(i, j, k, length)
					bricks <- rbind(bricks, bricksnew)
				}
			}
			#taking care of 2-1 w/ 5 centers also being counted in 2-1 w/ 4 or 3 centers
			if(length(bricks$length)> 1){
				for(a in 2:length(bricks$length)){
					for (b in 1:(a-1)){
						bricks$length[a] <- bricks$length[a] - (bricks$k[b]-bricks$k[a] +1)*bricks$length[b]
					}
				}
			}
			brickstotal <- rbind(brickstotal,bricks)
			bricks <- data.frame()
		}
	}
}

#added this condition because I broke everything with WhyDox(5,5,4)
if(length(brickstotal) > 0){
	#add a k choose C column for number of ways C points can be chosen in those lines
	brickstotal$comb <- choose(brickstotal$k,C)
	#length is number of lines for that i,j,k.  x2 to account for \ vs /
	brickstotal$total <- 2*brickstotal$length*brickstotal$comb

	#add the thing
	bricksfinal <- sum(brickstotal$total)
} else{
	bricksfinal <- 0
}

############################################
## The End
############################################

#yay
total <- choose(M*N,C)
result <- round(100*(horizontal + vertical + diagonal + bricksfinal)/total,2)
return(result)
}

M <- 20
N <- 20
C <- 3
WhyDox(M,N,C)

M <- 4
N <- 3
C <- 3