# Scene Description:

This scene demonstrates how the JSON engine can check for, create, and read files through a series of sequential operations.

## Timeline

### Step 1: **Initial File Existence Check** (`does_MyFile_exist.json`)

```json
{
    "begin":
    [
        {"print": "$(does_file_exist ['My File.txt'])"},

        {
            "if": 
            [
                "$(does_file_exist ['My File.txt'])",
                {
                    "true": "Yes",
                    "false": "No"
                }
            ]
        }
    ],

    "Yes": 
    [
        {
            "print": "Yes, the file does exist"
        }
    ],

    "No": 
    [
        {
            "print": "No, the file does not exist"
        }
    ]
}
```

**Process:**
1. First, checks if `My File.txt` exists and prints the boolean result
2. Evaluates the condition:
   - If `True`: Executes the 'Yes' function, printing "Yes, the file does exist"
   - If `False`: Executes the 'No' function, printing "No, the file does not exist"

**Output:** `False` - The file does not exist yet

---

### Step 2: **File Creation** (`make_MyFile.json`)

```json
{
    "begin": 
    [
        {
            "write_string_to_file": 
            [
                "My File.txt",
                "Hello from json!"
            ]
        }
    ]
}
```

**Action:** Creates `My File.txt` with the content "Hello from json!"
**Output:** (No visible output - file is created silently)

---

### Step 3: **Secondary File Existence Check** (`does_MyFile_exist.json`)

**Code:** (Same as Step 1, but this time the 'Yes' branch executes)

**Output:** `True` - The file now exists after creation

---

### Step 4: **File Content Reading**

```json
{
    "begin": 
    [
        {
            "print": "$(read_file ['My File.txt'])"
        }
    ]
}
```

**Action:** Reads and prints the contents of `My File.txt`

**Output:** `Hello from json!` - Successfully reads the file content

---

## Summary

This sequence demonstrates four fundamental file operations:
1. **Checking** if a file exists
2. **Creating** a file with content
3. **Verifying** the file exists after creation
4. **Reading** the file content back

