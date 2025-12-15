# Gojo Lang

<div align="center">

![Version](https://img.shields.io/badge/version-6.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-purple.svg)

**A minimalist scripting language interpreter inspired by Gojo Satoru** 

*"Throughout Heaven and Earth, I alone am the honored one."*

</div>

---

## Features

| Feature | Syntax | Description |
|---------|--------|-------------|
| **Variables** | `int`, `string`, `double`, `bool`, `char` | Strongly typed variables |
| **Arrays** | `int[]`, `string[]` | Array support |
| **Output** | `print`, `println` | Console output |
| **Conditionals** | `if` / `else` / `finn` | Conditional branching |
| **While Loop** | `while` / `end` | While loops |
| **For Loop** | `for ... to ... but step` / `con` | For loops with custom step |
| **String Formatting** | `"Hello {name}"` | Inline expression evaluation |
| **Operators** | `isnt`, `&&`, `\|\|`, `!` | Logical operators |

## Installation

```bash
git clone https://github.com/cekYc/gojo_lang.git
cd gojo-lang
```

No dependencies required! Just Python 3.8+.

## Usage

```bash
python3 src/main.py <filename.gj>
```

### Example

```bash
python3 src/main.py examples/example.gj
```

## Syntax Guide

### Variables

```gojo
int x = 10
string name = "Gojo"
double pi = 3.14
bool active = true
char letter = "A"
```

### Output

```gojo
print "Hello "
println "World!"
println "Value: {x * 2}"
```

### Conditionals

```gojo
if x > 5
    println "Big"
else
    println "Small"
finn
```

### Loops

```gojo
# For loop (1 to 10)
for i = 1 to 10
    println "Count: {i}"
con

# For loop with step
for i = 10 to 1 but -1
    println "Countdown: {i}"
con

# While loop
while x < 100
    x = x + 1
end
```

### Operators

```gojo
if x isnt 0          # x != 0
if a && b            # a and b
if a || b            # a or b
if !flag             # not flag
```

## Project Structure

```
gojo-lang/
├── src/
│   └── main.py          # Interpreter
├── examples/
│   └── example.gj       # Example program
├── README.md
├── LICENSE
└── .gitignore
```

## Example Output

```
🚀 Gojo v6.0 (Isnt Update) Çalışıyor: examples/example.gj

------------------------------
=== GOJO LANG :: example.gj ===
Mode: Infinity
Charging Hollow Purple...

[5] Stabilizing vectors...
[4] Stabilizing vectors...
[3] Stabilizing vectors...
[2] Stabilizing vectors...
[1] Stabilizing vectors...

Blue + Red -> Purple

#  power=1
##  power=4
###  power=9

>>> HOLLOW PURPLE: 125 <<<
------------------------------
```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with 💜 and Hollow Purple energy**

</div>
