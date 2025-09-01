# 5_containers

Goal: Reproducible runs with Docker locally and Apptainer/Singularity on HPC.

## Docker (local)

```bash
# from repo root
docker build -t velo:latest -f 5_containers/Dockerfile .
# run stage 4 script using the image
docker run --rm -v "$PWD:$PWD" -w "$PWD" velo:latest \
  python 4_cluster_slurm/run_one.py --params 4_cluster_slurm/params.csv \
  --row-index 0 --out-dir 4_cluster_slurm/results
```

## Apptainer/Singularity (HPC)

Option A (build from Docker Hub image if accessible):

```bash
# on a machine with apptainer and internet
apptainer build containers/velo.sif 5_containers/velo.def
```

Then on the cluster:

```bash
apptainer exec --bind "$PWD:$PWD" containers/velo.sif \
  python 4_cluster_slurm/run_one.py --params 4_cluster_slurm/params.csv \
  --row-index 0 --out-dir 4_cluster_slurm/results
```
