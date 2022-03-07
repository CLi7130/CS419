#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <dlfcn.h>
#include <string.h>

// Name: Craig Li
// netID: craigli
// RUID: 133000399
// your code for readdir goes here

/*
Your assignment is to create an alternate version of the readdir Linux library function that will:
    - Call the real version of readdir
    - Check if the returned file name matches the name in the environment 
            variable HIDDEN
    - If it does, call readdir again to skip over this file entry.
    - Return the file data to the calling program.

*/
struct dirent *readdir(DIR *dirp){

    struct dirent *(*original_readdir)(DIR *dirp);
    original_readdir = dlsym(RTLD_NEXT, "readdir");

    //call real version of readdir
    struct dirent *file = original_readdir(dirp);
    char *hidden_list = getenv("HIDDEN");

    if(file == NULL || hidden_list == NULL){
        //error checking
        return NULL;
    }
    //extra credit implementation using strtok
    //assumes we don't have ':' char somehow in the filename
    //copies hidden_list because tokens modify string, preserve
    //the original in case.
    char temp_list[strlen(hidden_list)];
    strcpy(temp_list, hidden_list);
    char* token = strtok(temp_list, ":");
    
    /*
    //non extra credit implementation
    if(strcmp(hidden_list, file->d_name) == 0){
        file = original_readdir(dirp);
    }
     */
    //extra credit implementation
    while(token != NULL){
        //check each hidden filename against current filename
        if(strcmp(token, file->d_name) == 0){
            //increment to next file, then reset token list
            //so we can check the next file to see if it's also in the hidden
            //list - this continues until we find the next file that's not in
            //the hidden list, and this file is eventually returned
            file = original_readdir(dirp);
            strcpy(temp_list, hidden_list);
            token = strtok(temp_list, ":");
        }
        else{
            //go to next hidden filename
            token = strtok(NULL, ":");
        }
    }
    return (struct dirent *) file;
}