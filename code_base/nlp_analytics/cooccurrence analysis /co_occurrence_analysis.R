options(stringsAsFactors = FALSE)
library(quanteda) 
library(tokenizers)
install.packages("ggplotify")
library(ggplotify)
 

# Guardian data 
Guardian_path_to_subtopics_folder <- './code_base/evaluation/guardian/subtopics_data/'
Guardaian_path_to_save_cooccurrence_data <- './code_base/evaluation/guardian/cooccurance Analysis/'


# BBC 
Bbc_path_to_subtopics_folder <- './code_base/evaluation/bbc/subtopics_data/'
Bbc_path_to_save_cooccurrence_data <- './code_base/evaluation/bbc/cooccurance Analysis/'

# Al Jazeera 
Aljazeera_path_subtopics_folder <- './code_base/evaluation/aljazerra/subtopics_data/'
Aljazeera_path_to_save_cooccurrence_data <- './code_base/evaluation/aljazerra/cooccurance Analysis/'


generate_cooccurrence_plots <- function(path_to_subtopics_folder,path_to_save_data_table) {
  
  # use list.files to get all files with .csv extension
  csv_files <- list.files(path_to_subtopics_folder, pattern = "*.csv")
  
  # Iterate over each file in the folder
  for (file in csv_files) {
        # Remove the .csv extension from the file name
        file_name <- sub(".csv", "", file)
    
        print("file name is")
        print(as.character(file_name))
        result <- paste0(path_to_subtopics_folder, file)
        print(result)
    
    data <- read.csv(result)
    sotu_corpus_new <- corpus(data$main_content_y, docnames = data$Unnamed..0_x,
                              docvars = data.frame(year = substr(data$date_y, 0, 4)))
    
    ndoc(sotu_corpus_new)
    doc_text <- as.character(sotu_corpus_new[[2]])
    
    # Get the first 200 characters of the document text
    substring(doc_text, 1, 5000)
    
    corpus_sentences <- corpus_reshape(sotu_corpus_new, to = "sentences")
    
    print(ndoc(corpus_sentences))
    
    as.character(corpus_sentences[[1]])
    
    lemma_data <- read.csv("baseform_en.tsv", encoding = "UTF-8")
    
    # read an extended stop word list
    stopwords_extended <- readLines("stopwords_en.txt",encoding = "UTF-8")
    
    
    # Preprocessing of the corpus of sentences
    corpus_tokens <- corpus_sentences %>%
      tokens(remove_punct = TRUE, remove_numbers = TRUE, remove_symbols = TRUE) %>%
      tokens_tolower() %>%
      tokens_replace(lemma_data$inflected_form, lemma_data$lemma,
                     valuetype = "fixed") %>%
      tokens_remove(pattern = stopwords_extended, padding = T)
    
    # calculate multi-word unit candidates
    sotu_collocations <- quanteda.textstats::textstat_collocations(corpus_tokens,
                                                                   min_count = 25)
    sotu_collocations <- sotu_collocations[1:250, ]
    #corpus_tokens <- tokens_compound(corpus_tokens, sotu_collocations)
    
    
    minimumFrequency <- 10
    # Create DTM, prune vocabulary and set binary values for
    # presence/absence of types
    binDTM <- corpus_tokens %>%
      tokens_remove("") %>%
      dfm() %>%
      dfm_trim(min_docfreq = minimumFrequency) %>%
      dfm_weight("boolean")
    
    
    # Matrix multiplication for cooccurrence counts
    coocCounts <- t(binDTM) %*% binDTM
    as.matrix(coocCounts[1:1, 1:1])
    
    source("calculate.R")
    numberOfCoocs <- 15
    coocTerm <- as.character(file_name)
    coocs <- calculateCoocStatistics(coocTerm, binDTM, measure = "LOGLIK")
    print(coocs[1:40])
    # convert the variable to a data frame
    my_df <- data.frame(names = names(coocs), values = coocs, row.names = NULL)
    # write the data frame to a CSV file-allegation
    result2 <- paste0(path_to_save_data_table, file)
    print("Hello world")
    write.csv(my_df, file = result2, row.names = FALSE)
    
    
    
    resultGraph <- data.frame(from = character(), to = character(),
                              sig = numeric(0))
    
    
    
    # The structure of the temporary graph object is equal to
    # that of the resultGraph
    tmpGraph <- data.frame(from = character(), to = character(),
                           sig = numeric(0))
    # Fill the data.frame to produce the correct number of
    # lines
    tmpGraph[1:numberOfCoocs, 3] <- coocs[1:numberOfCoocs]
    # Entry of the search word into the first column in all
    # lines
    tmpGraph[, 1] <- coocTerm
    # Entry of the co-occurrences into the second column of the
    # respective line
    tmpGraph[, 2] <- names(coocs)[1:numberOfCoocs]
    # Set the significances
    tmpGraph[, 3] <- coocs[1:numberOfCoocs]
    # Attach the triples to resultGraph
    resultGraph <- rbind(resultGraph, tmpGraph)
    # Iteration over the most significant numberOfCoocs
    # co-occurrences of the search term
    for (i in 1:numberOfCoocs) {
      # Calling up the co-occurrence calculation for term i
      # from the search words co-occurrences
      newCoocTerm <- names(coocs)[i]
      coocs2 <- calculateCoocStatistics(newCoocTerm, binDTM, measure = "LOGLIK")
      # print the co-occurrences
      coocs2[1:10]
      # Structure of the temporary graph object
      tmpGraph <- data.frame(from = character(), to = character(),
                             sig = numeric(0))
      tmpGraph[1:numberOfCoocs, 3] <- coocs2[1:numberOfCoocs]
      tmpGraph[, 1] <- newCoocTerm
      tmpGraph[, 2] <- names(coocs2)[1:numberOfCoocs]
      tmpGraph[, 3] <- coocs2[1:numberOfCoocs]
      # Append the result to the result graph
      resultGraph <- rbind(resultGraph, tmpGraph[2:length(tmpGraph[,
                                                                   1]), ])
    }  
    
    resultGraph[sample(nrow(resultGraph), 6), ]  
    
    require(igraph)
    # set seed for graph plot
    set.seed(1)
    # Create the graph object as undirected graph
    graphNetwork <- graph.data.frame(resultGraph, directed = F)
    # Identification of all nodes with less than 2 edges
    verticesToRemove <- V(graphNetwork)[degree(graphNetwork) < 2]
    # These edges are removed from the graph
    graphNetwork <- delete.vertices(graphNetwork, verticesToRemove)
    # Assign colors to nodes (search term blue, others orange)
    V(graphNetwork)$color <- ifelse(V(graphNetwork)$name == coocTerm, 'cornflowerblue', 'orange')
    # Set edge colors
    E(graphNetwork)$color <- adjustcolor("DarkGray", alpha.f = .5)
    # scale significance between 1 and 10 for edge width
    E(graphNetwork)$width <- scales::rescale(E(graphNetwork)$sig, to = c(1, 10))
    
    # Set edges with radius
    E(graphNetwork)$curved <- 0.15
    # Size the nodes by their degree of networking (scaled between 5 and 15)
    V(graphNetwork)$size <- scales::rescale(log(degree(graphNetwork)), to = c(5, 15))
    # Define the frame and spacing for the plot
    par(mai=c(0,0,1,0))
    # Final Plot
    plot(
      graphNetwork,
      layout = layout.fruchterman.reingold,
      main = paste(coocTerm, 'Graph'),
      vertex.label.family = "sans",
      vertex.label.cex = 0.5,
      vertex.shape = "circle",
      vertex.label.dist = 0.5,#Labels of the nodes moved slightly
      vertex.frame.color = adjustcolor("darkgray", alpha.f = .5),
      vertex.label.color = 'black',#Color of node names
      vertex.label.font = 2,#Font of node names
      vertex.label = V(graphNetwork)$name,#node names
      vertex.label.cex = 1 #font size of node names
    )
    
    
    
    
    
    
    
    
  }
  

}

generate_cooccurrence_plots(Guardian_path_to_subtopics_folder,Guardaian_path_to_save_cooccurrence_data)
generate_cooccurrence_plots(Bbc_path_to_subtopics_folder,Bbc_path_to_save_cooccurrence_data)
generate_cooccurrence_plots(Aljazeera_path_subtopics_folder,Aljazeera_path_to_save_cooccurrence_data)


 