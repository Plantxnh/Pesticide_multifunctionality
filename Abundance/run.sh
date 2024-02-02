bwa index database.nucl.fa
python reads_qc.py -i fq.list -o fastq_qc -t 4 -f fastp_path
python get_rpkm_list.py fastq_qc input.rpkm.list
python reads_rpkm.py database.nucl.fa input.rpkm.list align_result map
sh align_result/shell/run.sh
python reads_rpkm.py database.nucl.fa input.rpkm.list align_result rpkm
