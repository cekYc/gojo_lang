# core.py
import os
import re
from state import memory, var_types
from stdlib import builtins
from utils import clean_expr, parse_value, format_text

def run_gojo(filename):
    if not os.path.exists(filename):
        print(f"❌ HATA: '{filename}' bulunamadı.")
        return

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    print(f"🚀 Gojo v7.0 (Modular) Çalışıyor: {filename}\n")
    print("-" * 30)
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Yorum temizleme
        in_string = False
        comment_pos = -1
        for idx, ch in enumerate(line):
            if ch == '"' and (idx == 0 or line[idx-1] != '\\'):
                in_string = not in_string
            elif ch == '#' and not in_string:
                comment_pos = idx
                break
        if comment_pos != -1:
            line = line[:comment_pos].strip()
        if not line:
            i += 1
            continue

        first_word = line.split()[0]

        # 1. TANIMLAMA
        base_types = ['int', 'string', 'double', 'bool', 'char']
        if (first_word in base_types) or first_word.endswith('[]') or first_word == 'array[]':
            tip = first_word
            if ',' in line and '=' not in line:
                vars_part = line[len(tip):].strip()
                var_list = [v.strip() for v in vars_part.split(',')]
                for var_name in var_list:
                    if tip.endswith('[]') or tip == 'array[]': memory[var_name] = []
                    elif tip == 'int': memory[var_name] = 0
                    elif tip == 'string': memory[var_name] = ""
                    elif tip == 'double': memory[var_name] = 0.0
                    elif tip == 'bool': memory[var_name] = False
                    elif tip == 'char': memory[var_name] = ''
                    var_types[var_name] = tip
            elif '=' in line:
                parts = line.split('=', 1)
                sol = parts[0].strip().split()
                sag = parts[1].strip()
                tip, isim = sol[0], sol[1]
                try:
                    if sag.startswith('input'):
                        soru = sag[5:].strip().strip('"') if len(sag) > 5 else ""
                        val = input(soru + " ")
                        memory[isim] = parse_value(tip, f'"{val}"')
                    else:
                        memory[isim] = parse_value(tip, sag)
                    var_types[isim] = tip
                except Exception as e:
                    print(f"❌ HATA (Satır {i+1}): {e}")
                    return
            else:
                parts = line.split()
                if len(parts) > 1:
                    var = parts[1]
                    if tip.endswith('[]') or tip == 'array[]': memory[var] = []
                    elif tip == 'int': memory[var] = 0
                    elif tip == 'string': memory[var] = ""
                    elif tip == 'double': memory[var] = 0.0
                    elif tip == 'bool': memory[var] = False
                    elif tip == 'char': memory[var] = ''
                    var_types[var] = tip

        # 1.b ADD (yeni söz dizimi: add((var) <değer>) — parantezli değişken adı kabul edilir)
        elif first_word == 'add':
            parts = line.split(None, 2)
            if len(parts) < 3:
                print(f"HATA: add kullanım: add((degisken) <değer>)")
            else:
                raw = parts[1].strip()
                # allow caller to write add((var) or add((var)) or old add var
                varname = raw.lstrip('(').rstrip(')')
                expr = parts[2]
                if varname in memory and isinstance(memory[varname], list):
                    vtip = var_types.get(varname, None)
                    try:
                        if vtip and vtip.endswith('[]') and vtip != 'array[]':
                            val = parse_value(vtip.replace('[]',''), expr)
                        else:
                            val = eval(clean_expr(expr), builtins, memory)
                        memory[varname].append(val)
                    except Exception as e:
                        print(f"Add hatasi: {e}")

        # 1.c APPEND (+=)
        elif '+=' in line and first_word not in ['if', 'while', 'for', 'print', 'println', 'con']:
            try:
                parts = line.split('+=',1)
                varname = parts[0].strip()
                expr = parts[1].strip()
                if varname in memory:
                    if isinstance(memory[varname], list):
                         val = eval(clean_expr(expr), builtins, memory)
                         if isinstance(val, list): memory[varname].extend(val)
                         else: memory[varname].append(val)
                    else:
                         val = eval(clean_expr(expr), builtins, memory)
                         memory[varname] += val
            except Exception as e: print(f"Atama hatasi: {e}")

        # 2. GÜNCELLEME (=)
        elif '=' in line and first_word not in ['if', 'while', 'for', 'print', 'println', 'con', 'add'] + base_types:
            parts = line.split('=', 1)
            var_expr, expr = parts[0].strip(), parts[1].strip()
            try:
                if '[' in var_expr and ']' in var_expr: 
                    base_name = var_expr.split('[')[0]
                    if base_name in memory:
                        val = eval(clean_expr(expr), builtins, memory)
                        mevcut = eval(var_expr, builtins, memory)
                        if isinstance(mevcut, int) and not isinstance(mevcut, bool): val = int(val)
                        elif isinstance(mevcut, float): val = float(val)
                        # val yerine repr(val) kullanıyoruz ki stringlerin tırnakları korunsun
                        exec(f"memory['{base_name}']{var_expr[len(base_name):]} = {repr(val)}")
                elif var_expr in memory:
                    if expr.startswith('input'):
                        soru = expr[5:].strip().strip('"') if len(expr) > 5 else ""
                        val = input(soru + " ")
                    else:
                        val = eval(clean_expr(expr), builtins, memory)
                    
                    eski = memory[var_expr]
                    if isinstance(eski, bool): val = str(val).lower() == 'true'
                    elif isinstance(eski, int): val = int(val)
                    elif isinstance(eski, float): val = float(val)
                    elif isinstance(eski, str): val = str(val)
                    memory[var_expr] = val
            except Exception as e: print(f"Atama hatasi: {e}")

        # 3. PRINT / PRINTLN
        elif first_word == 'print':
            try:
                res = eval(clean_expr(line[5:].strip()), builtins, memory)
                print(f"{format_text(str(res))}", end='', flush=True)
            except Exception as e: print(f"HATA: {e}")
        elif first_word == 'println':
            if len(line.strip()) == 7: print()
            else:
                try:
                    res = eval(clean_expr(line[7:].strip()), builtins, memory)
                    print(f"{format_text(str(res))}")
                except: print(f"HATA: Yazdirma hatasi")

        # 4. FOR
        elif first_word == 'for':
            try:
                match = re.search(r'for\s+(\w+)\s*=\s*(.+?)\s+to\s+(.+?)(?:\s+but\s+(.+))?$', line)
                if match:
                    var_name = match.group(1)
                    start = int(eval(match.group(2), builtins, memory))
                    end = int(eval(match.group(3), builtins, memory))
                    step = 1
                    if match.group(4): step = int(eval(match.group(4), builtins, memory))
                    memory[var_name] = start
                    
                    skip = False
                    if step > 0 and start > end: skip = True
                    elif step < 0 and start < end: skip = True
                    
                    if skip:
                        nested = 0
                        while i < len(lines):
                            i += 1
                            if i >= len(lines): break
                            curr = lines[i].strip().split()[0]
                            if curr == 'for': nested += 1
                            elif curr == 'con':
                                if nested == 0: break
                                nested -= 1
            except: pass

        # 5. CON
        elif first_word == 'con':
            nested = 0
            temp_i = i - 1
            while temp_i >= 0:
                s_line = lines[temp_i].strip()
                if not s_line: 
                    temp_i -= 1
                    continue
                s_word = s_line.split()[0]
                if s_word == 'con': nested += 1
                elif s_word == 'for':
                    if nested == 0:
                        match = re.search(r'for\s+(\w+)\s*=\s*(.+?)\s+to\s+(.+?)(?:\s+but\s+(.+))?$', s_line)
                        if match:
                            var = match.group(1)
                            end = int(eval(match.group(3), builtins, memory))
                            step = 1
                            if match.group(4): step = int(eval(match.group(4), builtins, memory))
                            
                            memory[var] += step
                            curr = memory[var]
                            cont = False
                            if step > 0 and curr <= end: cont = True
                            elif step < 0 and curr >= end: cont = True
                            
                            if cont: i = temp_i
                            break
                    else: nested -= 1
                temp_i -= 1

        # 6. IF
        elif first_word == 'if':
             try:
                cond = eval(clean_expr(line[2:].strip()), builtins, memory)
                if not cond:
                    nested = 0
                    while i < len(lines):
                        i += 1
                        if i >= len(lines): break
                        curr = lines[i].strip().split()[0]
                        if curr == 'if': nested += 1
                        elif curr == 'finn':
                            if nested == 0: break
                            nested -= 1
                        elif curr == 'else':
                            if nested == 0: break
             except Exception as e:
                 print(f"❌ IF HATASI (Satır {i+1}): {e}")
                 return

        # 7. ELSE
        elif first_word == 'else':
             nested = 0
             while i < len(lines):
                i += 1
                if i >= len(lines): break
                curr = lines[i].strip().split()[0]
                if curr == 'if': nested += 1
                elif curr == 'finn':
                    if nested == 0: break
                    nested -= 1

        # 8. WHILE
        elif first_word == 'while':
             try:
                 if not eval(clean_expr(line[5:].strip()), builtins, memory):
                     nested = 0
                     while i < len(lines):
                         i += 1
                         if i >= len(lines): break
                         curr = lines[i].strip().split()[0]
                         if curr == 'while': nested += 1
                         elif curr == 'end':
                             if nested == 0: break
                             nested -= 1
             except Exception as e:
                 print(f"❌ WHILE HATASI (Satır {i+1}): {e}")
                 return

        elif first_word == 'finn': pass
        elif first_word == 'end':
            temp_i = i - 1
            while temp_i >= 0:
                s = lines[temp_i].strip()
                if not s: 
                    temp_i -= 1
                    continue
                if s.startswith('while') and 'end' not in lines[temp_i:i]:
                    if eval(clean_expr(s[5:].strip()), builtins, memory): i = temp_i
                    break
                temp_i -= 1

        i += 1
    print("\n" + "-" * 30)