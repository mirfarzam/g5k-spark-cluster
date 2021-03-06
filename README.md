# Grid’5000 Apache Spark Cluster 

This script will deploy a basic Apache Spark Cluster in our reserved nodes in Grid’5000. Hope to improve it in the future, any help is welcomed.

## Dependencies ##

* Python 3.x


## How to run it ##

First of all we have to clone this repository in the frontend node in Grid’5000.

> **Download the disk image and the env file from [here](http://i3s.unice.fr/~pagliari/downloads/g5k-images), then move them inside the repository folder.**

### Reserve resources ###

To reserve nodes in Grid’5000 you just have to run the following command (adapted to your situation):
```shell
frontend > oarsub -t deploy -p "cluster='suno'" -I -l nodes=4,walltime=2 -k
```
In this example we are in the Sophia region, we’re requesting _4_ nodes for _2_ hours in the cluster named _”suno”_.

For further and more specific information follow the Grid’5000’s [Getting Started tutorial](https://www.grid5000.fr/mediawiki/index.php/Getting_Started).

### Pre-tasks ###

#### Prepare the config file ####

Open the file `config.conf` and modify the parameters to comply your system configuration (g5k, spark and folders).
Be sure to change the username with your grid5000 username.

#### Install Spark in your frontend ####

Download ad extract a binary of Spark ([download 2.2.4](https://archive.apache.org/dist/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz)) in your frontend home.

### Run it ###

```shell
frontend > python3 deploy.py
```

To access your nodes use:
```shell
ssh root@node-name
```

That’s all. Simple, no?

## Post-Run ##

### Connect to Spark Master Dashboard ###

To connect to the Web UI, we need to open an ssh tunnel to the web service port:

```shell
localhost > ssh {{ g5k.username }}@access.grid5000.fr -N -L8080:{{ nimbus_node_address }}:8080

```

Now the Web Server should be reached through `localhost:8080`

## Multi-Cluster Run ##

The script is able to deploy storm also in a multi-cluster environment. To make the reservation use:

```shell
frontend > oargridsub -t deploy -w '0:59:00' suno:rdef="/nodes=6",parapide:rdef="/nodes=6"
```

In this case, we don't enter in the job shell, so we don't have the `OAR_NODE_FILE` systemvariable. We can retrieve the list of the reserved machines using:

```shell
frontend > oargridstat -w -l {{ GRID_RESERVATION_ID  }} | sed '/^$/d' > ~/machines
```

Finally, change the configuration file specifying the location of the file just created (`oar.file.location=~/machines`) and write "yes" in the multi cluster option (`multi.cluster=yes`).

For more informations visit the Grid'5000's [Multi-site jobs](https://www.grid5000.fr/mediawiki/index.php/Advanced_OAR#Multi-site_jobs_with_OARGrid) tutorial.

## More

> Check out also the other script for:
> * [**Apache Storm**](https://github.com/ale93p/g5k-storm-cluster)
> * [**Apache Flink**](https://github.com/ale93p/g5k-flink-cluster)


