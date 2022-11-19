# Examples

## more details

[MkDocs](https://www.mkdocs.org/user-guide/#user-guide)

## admonitions

!!! note

    Simple.

!!! note "Title"

    With title.

!!! note ""

    Plain.

??? note "Collapsible"

    Functionality from `pymdownx.details` extension.

!!! info inline end

    Inline at end.

```python
# nothing.py
"""This module does absolutely nothing"""

import this
```

!!! info inline

    Inline at beginning.

```python
# nothing.py
"""This module does absolutely nothing"""

import this
```

### admonition types

!!! note

    `note`

!!! abstract

    `abstract`, `summary` or `tldr`

!!! info

    `info` or `todo`

!!! tip

    `tip`, `hint` or `important`

!!! success

    `success`, `check` or `done`

!!! question

    `question`, `help` or `faq`

!!! warning

    `warning`, `caution` or `attention`

!!! failure

    `failure`, `fail` or `missing`

!!! danger

    `danger` or `error`

!!! bug

    `bug`

!!! example

    `example`

!!! quote

    `quote` or `cite`

## code blocks

### simple

```py
import this
```

### title

```py title="with title"
import this
```

### line numbers

```py title="starting from 1" linenums="1"
import this
```

```py title="starting from 2" linenums="2"
import this
```

### highlighted lines

`pymarkdownx.highlight`

```py title="highlighted lines" linenums="1" hl_lines="1 4"
import this
import random

rand = random.random()
```

### inline highlights

`pymarkdownx.inlinehilite`

This text has an inline highlight: `#!py range()`

### embedded external file

`pymarkdownx.snippets`

```py title="orm.py"
--8<-- "src/lib/orm.py"
```

## tables

| Method      | Description                          |
| ----------- | ------------------------------------ |
| `GET`       | :material-check:     Fetch resource  |
| `PUT`       | :material-check-all: Update resource |
| `DELETE`    | :material-close:     Delete resource |

## diagrams

### flow chart

``` mermaid
graph LR
  A[Start] --> B{Error?};
  B -->|Yes| C[Hmm...];
  C --> D[Debug];
  D --> B;
  B ---->|No| E[Yay!];
```

### sequence

``` mermaid
sequenceDiagram
  Alice->>John: Hello John, how are you?
  loop Healthcheck
      John->>John: Fight against hypochondria
  end
  Note right of John: Rational thoughts!
  John-->>Alice: Great!
  John->>Bob: How about you?
  Bob-->>John: Jolly good!
```

### state

``` mermaid
stateDiagram-v2
  state fork_state <<fork>>
    [*] --> fork_state
    fork_state --> State2
    fork_state --> State3

    state join_state <<join>>
    State2 --> join_state
    State3 --> join_state
    join_state --> State4
    State4 --> [*]
```

### class

``` mermaid
classDiagram
  Person <|-- Student
  Person <|-- Professor
  Person : +String name
  Person : +String phoneNumber
  Person : +String emailAddress
  Person: +purchaseParkingPass()
  Address "1" <-- "0..1" Person:lives at
  class Student{
    +int studentNumber
    +int averageMark
    +isEligibleToEnrol()
    +getSeminarsTaken()
  }
  class Professor{
    +int salary
  }
  class Address{
    +String street
    +String city
    +String state
    +int postalCode
    +String country
    -validate()
    +outputAsLabel()
  }
```

### entity relationship

``` mermaid
erDiagram
  CUSTOMER ||--o{ ORDER : places
  ORDER ||--|{ LINE-ITEM : contains
  CUSTOMER }|..|{ DELIVERY-ADDRESS : uses
```
