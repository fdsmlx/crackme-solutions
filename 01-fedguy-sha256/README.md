# Crackme Solution: FedGuy SHA256

**Date:** 2025-11-21
**Difficulty:** Easy
**Time:** ~40 minutes
**Status:** SOLVED
**Source:** [crackmes.one](https://crackmes.one/crackme/691abffc2d267f28f69b7e8a)

---

## File Info

| Property | Value |
| --- | --- |
| Filename | crack |
| Type | ELF 64-bit LSB pie executable |
| Compiler | GCC 15.2.1 |
| Protection | SHA256 hash comparison |
| Solution | chicken |

---

## Reconnaissance

```bash
file crack
# crack: ELF 64-bit LSB pie executable, x86-64

strings crack | grep -i "pass\|key"
# no results

objdump -t crack | grep -i "debug"
# no debug symbols
```

Clean binary, no obvious strings.

---

## Static Analysis

### Decompiled main() from IDA Pro

```c
int main() {
  char input[32];
  char hash[32];
  char hex[72];

  printf("Input Password: ");
  scanf("%s", input);

  SHA256(input, strlen(input), hash);
  bytes_to_hex(hash, 32, hex);

  if (!strcmp("811eb81b9d11d65a36c53c3ebdb738ee303403cb79d781ccf4b40764e0a9d12a", hex))
    puts("You win :)");
  else
    puts("You lose :(");
}
```

Algorithm:
1. Read input
2. SHA256 hash
3. Compare with: `811eb81b9d11d65a36c53c3ebdb738ee303403cb79d781ccf4b40764e0a9d12a`

---

## Attack

### Attempt 1: Online databases

Tried CrackStation and hashes.com - found immediately.

### Attempt 2: Hashcat bruteforce

```bash
hashcat -m 1400 -a 3 hash.txt ?l?l?l?l?l?l?l --increment
```

Found in 8 seconds at 10% progress (4.1 GH/s on GPU).

Password charset: lowercase, 7 chars
Search space: 26^7 = 8,031,810,176

---

## Solution

Password: **chicken**

Verification:
```bash
echo "chicken" | ./crack
# Input Password: You win :)
```

```python
import hashlib
hashlib.sha256(b"chicken").hexdigest()
# 811eb81b9d11d65a36c53c3ebdb738ee303403cb79d781ccf4b40764e0a9d12a
```

---

## Timeline

```
00:00 - First run
00:05 - IDA Pro analysis
00:15 - Algorithm understood
00:20 - Online databases -> found
00:30 - Hashcat setup (Windows GPU)
00:36 - Bruteforce -> cracked
00:40 - Verified
```

---

## Notes

SHA256 is irreversible - can't write a keygen. Only option is bruteforce/dictionary/rainbow tables.

First SHA256 crackme. Found online easily but wanted to practice hashcat with GPU bruteforce. 

---

## Screenshots

![IDA Pro decompilation](https://raw.githubusercontent.com/fdsmlx/crackme-solutions/main/resources/Pasted%20image%2020251121110351.png)

![Hashcat cracking](https://raw.githubusercontent.com/fdsmlx/crackme-solutions/main/resources/Pasted%20image%2020251121110403.png)
