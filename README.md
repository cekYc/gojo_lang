# Gojo Lang

<div align="center">

![Version](https://img.shields.io/badge/version-7.0-red.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-purple.svg)
![Build](https://img.shields.io/badge/build-modular-orange.svg)

**A minimalist, Turing-complete interpreted language inspired by Gojo Satoru.**

*"Throughout Heaven and Earth, I alone am the honored one."*

</div>

---

## 🚀 What is New in v7.0 (The Limitless Update)?
- **Modular Architecture:** The core engine has been refactored into modular components (`core`, `state`, `stdlib`).
- **Standard Library:** Built-in support for Math (`sqrt`, `pow`, `abs`) and Randomness (`random`).
- **Dynamic Memory:** Full support for dynamic arrays using `add` and `len`.
- **Enhanced Logic:** Improved parser stability and memory management.

---

## Features

| Feature | Syntax | Description |
|---------|--------|-------------|
| **Variables** | `int`, `string`, `double`, `bool` | Strongly typed variables |
| **Dynamic Arrays** | `array[]`, `add`, `len()` | List manipulation |
| **Math & Random** | `sqrt()`, `pow()`, `random()` | Built-in standard library |
| **Output** | `print`, `println` | Console output |
| **Conditionals** | `if` / `else` / `finn` | Conditional branching |
| **Loops** | `while`, `for ... to ...` | Iterative loops |
| **Formatting** | `"Value: {x}"` | Inline expression evaluation |
| **Operators** | `isnt`, `&&`, `||`, `!` | Logical operators |

## Installation

```bash
git clone [https://github.com/cekYc/gojo_lang.git](https://github.com/cekYc/gojo_lang.git)
cd gojo-lang
```

No dependencies required! Just Python 3.8+.

## Usage

```bash
python3 src/main.py <filename.gj>
```

### Example

```bash
python3 src/main.py examples/moduler_test.gj
```

## Syntax Guide

## Math & Random (New!)

'''gojo
Random number generation
int luck = random(1, 100)
Math functions
double root = sqrt(144)    # 12.0
double power = pow(2, 5)   # 32.0
int absolute = abs(-50)    # 50
'''

## Dynamic Arrays (New!)

'''gojo
Define a dynamic array
array[] basket = []

Add items
add basket "Apple"
add basket "Banana"

Get length
println "Items count: {len(basket)}"
'''

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
│   ├── main.py          # Entry point
│   ├── core.py          # Interpreter Engine
│   ├── state.py         # Memory Management
│   ├── stdlib.py        # Standard Library (Math/Random)
│   └── utils.py         # Parser Utilities
├── examples/
│   └── test.gj          # Full feature test
├── README.md
├── LICENSE
└── .gitignore
```

## Example Output

```
🚀 Gojo v7.0 (Modular Update) Çalışıyor: examples/example.gj

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
