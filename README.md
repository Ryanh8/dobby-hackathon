flowchart TB
    subgraph "Slack Channel"
        User[/"👤 User Message"/]
        BossMsg["👔 Boss Bot Message"]
        HRMsg["💅 HR Bot Message"]
    end

    subgraph "Message Queue"
        Queue[(Message Queue)]
        Processor{"🔄 Message<br>Processor"}
    end

    subgraph "Boss Bot Agent"
        BossAI["🤖 Boss Bot AI<br>Micromanaging Personality"]
        BossPrompts["📝 Boss Random Prompts<br>'TPS Reports!'<br>'Team Synergy!'"]
    end

    subgraph "HR Bot Agent"
        HRAI["🤖 HR Bot AI<br>Gen Z Personality"]
        HRPrompts["📝 HR Random Prompts<br>'slay bestie!'<br>'fr fr no cap'"]
    end

    User --> Queue
    BossMsg --> Queue
    HRMsg --> Queue
    Queue --> Processor

    Processor -->|User Message| BossAI & HRAI
    Processor -->|Boss Message| HRAI
    Processor -->|HR Message| BossAI

    BossAI --> BossMsg
    HRAI --> HRMsg
    BossPrompts -.->|Random| BossAI
    HRPrompts -.->|Random| HRAI

    style User fill:#85C1E9
    style Queue fill:#F9E79F
    style Processor fill:#F9E79F
    style BossAI fill:#82E0AA
    style HRAI fill:#82E0AA
    style BossMsg fill:#D7BDE2
    style HRMsg fill:#D7BDE2
    style BossPrompts fill:#F8C471
    style HRPrompts fill:#F8C471