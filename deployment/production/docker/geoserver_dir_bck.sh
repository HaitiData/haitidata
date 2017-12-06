#!/bin/bash

SOURCE_DIR_PATH=/geoserver-dev-data-new
SOURCE_DIR_NAME=data
BCK_DIR=/home/ubuntu/geoserver_bck 

echo "*****************************************************************"
echo "-----------------------------------------------------------------"
echo "*****************************************************************"
echo $(date) "--> starting bck for geoserver data folder"

this_week_dir=$BCK_DIR/$(date +"%Yweek%W")
echo "checking backup folder -->" $this_week_dir

if [ -e $this_week_dir ]
then
  echo folder exists
  echo $(date) "--> creating incremental archive"
  sudo tar -cpzf $this_week_dir/incr_dump.tgz -C $SOURCE_DIR_PATH -g $this_week_dir/tarlog.snap --backup=numbered $SOURCE_DIR_NAME
  sudo cp $this_week_dir/tarlog_lev0.snap $this_week_dir/tarlog.snap
  echo $(date) "--> incremental archive created"
else
  echo creating folder
  mkdir $this_week_dir
  echo $(date) "--> creating full archive"
  sudo tar -cpzf $this_week_dir/full_dump.tgz -C $SOURCE_DIR_PATH -g $this_week_dir/tarlog.snap $SOURCE_DIR_NAME
  sudo cp $this_week_dir/tarlog.snap $this_week_dir/tarlog_lev0.snap
  echo $(date) "--> full archive created"
fi

# now deleting old folders

ws=$(echo 01)
for w in $(seq -w 5 4 52)
do
 ws=$(echo $ws"|"$w)
done

wre=$(echo "201[6-9]week("$ws")")
for dir in $(ls $BCK_DIR | head -n -3 | grep -Ev $wre)
do
 echo removing $dir
 sudo rm -r $(echo $BCK_DIR"/"$dir)
done

echo $(date) "--> end of backup procedure for geoserver data folder"
