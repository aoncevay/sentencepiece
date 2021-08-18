build=${1-build}

rm -r $build
mkdir $build
cd $build
cmake ..
make -j