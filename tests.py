#!/usr/bin/env python3

# TOOLS FOR TESTING
tools = {
    'dante' : "toolshed.g2.bx.psu.edu/repos/petr-novak/dante/dante/1.0.0",
    'gff_to_tabular' : "toolshed.g2.bx.psu.edu/repos/petr-novak/dante/gff_to_tabular/0.1.0",
    'gff_summary' : "toolshed.g2.bx.psu.edu/repos/petr-novak/dante/gff_summary/0.1.0",
    'gff_extract' : "toolshed.g2.bx.psu.edu/repos/petr-novak/dante/domains_extract/1.0.0",
    'domain_filter' : "toolshed.g2.bx.psu.edu/repos/petr-novak/dante/domains_filter/1.0.0",
    'paired_fastq_filtering' : 'toolshed.g2.bx.psu.edu/repos/petr-novak/re_utils/paired_fastq_filtering/1.0.0',
    'fasta_affixer' : "toolshed.g2.bx.psu.edu/repos/petr-novak/re_utils/fasta_affixer/1.0.0",
    'chip_seq_ratio' : "toolshed.g2.bx.psu.edu/repos/petr-novak/re_utils/chip_seq_ratio_1/0.1.1",
    'fasta_interlacer' : "toolshed.g2.bx.psu.edu/repos/petr-novak/re_utils/fasta_interlacer/1.0.0",
    'sampler' : "toolshed.g2.bx.psu.edu/repos/petr-novak/re_utils/sampler/1.0.0",
    'pair_scan' : "toolshed.g2.bx.psu.edu/repos/petr-novak/re_utils/pairScan/1.0.0",
    'rename_sequences' : "toolshed.g2.bx.psu.edu/repos/petr-novak/re_utils/rename_sequences/1.0.0",
    'fasta_input' : "toolshed.g2.bx.psu.edu/repos/petr-novak/re_utils/fasta_input/1.0.0",
    'rm_search' : "toolshed.g2.bx.psu.edu/repos/petr-novak/re_utils/RMsearch/1.0.1",
    'extract_contigs' : "toolshed.g2.bx.psu.edu/repos/petr-novak/re_utils/extract_contigs/1.0.0",
    'single_fasta_filtering' : "toolshed.g2.bx.psu.edu/repos/petr-novak/re_utils/single_fastq_filtering/1.0.0",
    'names_affixer' : "toolshed.g2.bx.psu.edu/repos/petr-novak/re_utils/names_affixer/1.0.0"
}
# FILES FOR TESTING
files_to_upload = {
    'fq1' : "test_data/ERR215189_1_part.fastq.gz",
    'fq2' : "test_data/ERR215189_2_part.fastq.gz",
    'gepy_genome' : "test_data/GEPY_test_long_1.fa",
    'aln_contigs' : "test_data/CL_38_35.aln",
    'gff_dante' : "test_data/dante_unfiltered_output.gff3"
}



