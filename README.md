# Terraform SG diff

Quickly knocked up script to turn:

```
...
      ingress.715696897.ipv6_cidr_blocks.#:  "0" => "0"
      ingress.715696897.prefix_list_ids.#:   "0" => "0"
      ingress.715696897.protocol:            "tcp" => "tcp"
      ingress.715696897.security_groups.#:   "1" => "5"
      ingress.715696897.self:                "false" => "false"
      ingress.715696897.to_port:             "443" => "443"
...
```

into::
    Added rule 443_tcp_10.0.0.0/8


## How to run

   python ./terraform-sg-diff.py
   *PASTE SG CHANGES*
   <Ctrl+D>

