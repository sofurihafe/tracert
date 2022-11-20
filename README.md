# Tracert(-like) tool
## Usage
`py tracert.py <flag & value>  target`

Supported flags:
- -h : maximum hops

Examples:
- `tracert.py duckduckgo.com`
- `tracert.py -h 5 duckduckgo.com`

```
> py tracert.py -h 5 ya.ru

0 192.168.0.1
1 192.168.0.1
2 217.197.4.1
3 172.24.31.5 
4 172.24.25.32
```

## License
#### GNU GPLv3
