
wget https://zenodo.org/record/5648048/files/seecer.tar.gz
tar -zxvf seecer.tar.gz
mv seecer third_party

export LD_LIBRARY_PATH=third_party/seecer/SEECER/lib:$LD_LIBRARY_PATH
