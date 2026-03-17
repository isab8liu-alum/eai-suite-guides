# 5. Troubleshooting

## DigitalOcean Installation Issues

Common causes: 

------------------------------------------------------------------------

## Cluster Bloom Issues

### Configuration Failed or Timed Out

Try rerunning Bloom:

``` bash
sudo ./bloom cli --config bloom.yaml
```

If issue persists: - Verify disk mapping (`/dev/vdc1`) - Ensure droplet
has sufficient resources - Confirm network access

------------------------------------------------------------------------

