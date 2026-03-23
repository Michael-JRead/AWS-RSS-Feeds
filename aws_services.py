"""
AWS service registry mapping service names to RSS feed URLs and filter keywords.

Feed sources:
  1. What's New feed — filtered by keywords per service
  2. Per-topic AWS blog feeds — direct RSS for that topic/service

Each entry:
  name     : Display name shown in the UI
  category : Grouping label
  keywords : Words matched (case-insensitive) against What's New item titles/descriptions
  feeds    : List of direct RSS feed URLs to scrape for this service
"""

WHATS_NEW_FEED = "https://aws.amazon.com/about-aws/whats-new/recent/feed/"

AWS_SERVICES = [
    # ── General / Cross-service ─────────────────────────────────────────────
    {
        "name": "AWS News Blog (All)",
        "category": "General",
        "keywords": ["aws"],
        "feeds": [
            "https://aws.amazon.com/blogs/aws/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "What's New (All Services)",
        "category": "General",
        "keywords": ["aws"],
        "feeds": [WHATS_NEW_FEED],
    },

    # ── Compute ─────────────────────────────────────────────────────────────
    {
        "name": "EC2 (Elastic Compute Cloud)",
        "category": "Compute",
        "keywords": ["ec2", "elastic compute cloud", "instance type", "ami", "ec2 instance"],
        "feeds": [
            "https://aws.amazon.com/blogs/compute/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "EC2 Auto Scaling",
        "category": "Compute",
        "keywords": ["ec2 auto scaling", "auto scaling group", "launch template"],
        "feeds": [
            "https://aws.amazon.com/blogs/compute/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "EC2 Image Builder",
        "category": "Compute",
        "keywords": ["ec2 image builder", "image builder"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "EC2 Spot Instances",
        "category": "Compute",
        "keywords": ["spot instance", "ec2 spot", "spot fleet"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Lambda",
        "category": "Compute",
        "keywords": ["lambda", "aws lambda", "serverless function"],
        "feeds": [
            "https://aws.amazon.com/blogs/compute/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "App Runner",
        "category": "Compute",
        "keywords": ["app runner", "aws app runner"],
        "feeds": [
            "https://aws.amazon.com/blogs/compute/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Elastic Beanstalk",
        "category": "Compute",
        "keywords": ["elastic beanstalk", "beanstalk"],
        "feeds": [
            "https://aws.amazon.com/blogs/compute/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Lightsail",
        "category": "Compute",
        "keywords": ["lightsail", "amazon lightsail"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Batch",
        "category": "Compute",
        "keywords": ["aws batch"],
        "feeds": [
            "https://aws.amazon.com/blogs/compute/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Outposts",
        "category": "Compute",
        "keywords": ["aws outposts", "outpost rack", "outpost server"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Snow Family",
        "category": "Compute",
        "keywords": ["snow family", "snowball", "snowcone", "snowmobile", "aws snow"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Wavelength",
        "category": "Compute",
        "keywords": ["aws wavelength", "wavelength zone"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Local Zones",
        "category": "Compute",
        "keywords": ["local zone", "aws local zones"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Compute Optimizer",
        "category": "Compute",
        "keywords": ["compute optimizer", "aws compute optimizer"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Serverless Application Repository",
        "category": "Compute",
        "keywords": ["serverless application repository", "sar"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Nitro Enclaves",
        "category": "Compute",
        "keywords": ["nitro enclaves", "aws nitro"],
        "feeds": [WHATS_NEW_FEED],
    },

    # ── Containers ───────────────────────────────────────────────────────────
    {
        "name": "ECS (Elastic Container Service)",
        "category": "Containers",
        "keywords": ["ecs", "elastic container service", "amazon ecs"],
        "feeds": [
            "https://aws.amazon.com/blogs/containers/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "EKS (Elastic Kubernetes Service)",
        "category": "Containers",
        "keywords": ["eks", "elastic kubernetes service", "amazon eks", "kubernetes"],
        "feeds": [
            "https://aws.amazon.com/blogs/containers/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "ECR (Elastic Container Registry)",
        "category": "Containers",
        "keywords": ["ecr", "elastic container registry", "container image"],
        "feeds": [
            "https://aws.amazon.com/blogs/containers/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Fargate",
        "category": "Containers",
        "keywords": ["fargate", "aws fargate"],
        "feeds": [
            "https://aws.amazon.com/blogs/containers/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "ECS Anywhere",
        "category": "Containers",
        "keywords": ["ecs anywhere"],
        "feeds": [
            "https://aws.amazon.com/blogs/containers/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "EKS Anywhere",
        "category": "Containers",
        "keywords": ["eks anywhere"],
        "feeds": [
            "https://aws.amazon.com/blogs/containers/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "App2Container",
        "category": "Containers",
        "keywords": ["app2container", "aws app2container"],
        "feeds": [WHATS_NEW_FEED],
    },

    # ── Storage ─────────────────────────────────────────────────────────────
    {
        "name": "S3 (Simple Storage Service)",
        "category": "Storage",
        "keywords": ["amazon s3", "simple storage service", "s3 bucket", "s3 object", "s3 storage"],
        "feeds": [
            "https://aws.amazon.com/blogs/storage/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "S3 Glacier",
        "category": "Storage",
        "keywords": ["s3 glacier", "glacier", "glacier deep archive"],
        "feeds": [
            "https://aws.amazon.com/blogs/storage/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "EBS (Elastic Block Store)",
        "category": "Storage",
        "keywords": ["ebs", "elastic block store", "ebs volume", "ebs snapshot"],
        "feeds": [
            "https://aws.amazon.com/blogs/storage/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "EFS (Elastic File System)",
        "category": "Storage",
        "keywords": ["efs", "elastic file system", "amazon efs"],
        "feeds": [
            "https://aws.amazon.com/blogs/storage/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "FSx",
        "category": "Storage",
        "keywords": ["amazon fsx", "fsx for lustre", "fsx for windows", "fsx for netapp", "fsx for openzfs"],
        "feeds": [
            "https://aws.amazon.com/blogs/storage/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Storage Gateway",
        "category": "Storage",
        "keywords": ["storage gateway", "aws storage gateway", "file gateway", "tape gateway"],
        "feeds": [
            "https://aws.amazon.com/blogs/storage/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "AWS Backup",
        "category": "Storage",
        "keywords": ["aws backup", "backup vault", "backup plan"],
        "feeds": [
            "https://aws.amazon.com/blogs/storage/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Elastic Disaster Recovery",
        "category": "Storage",
        "keywords": ["elastic disaster recovery", "aws drs", "disaster recovery"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "File Cache",
        "category": "Storage",
        "keywords": ["amazon file cache", "file cache"],
        "feeds": [WHATS_NEW_FEED],
    },

    # ── Database ─────────────────────────────────────────────────────────────
    {
        "name": "RDS (Relational Database Service)",
        "category": "Database",
        "keywords": ["amazon rds", "relational database service", "rds for mysql", "rds for postgresql", "rds for oracle"],
        "feeds": [
            "https://aws.amazon.com/blogs/database/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Aurora",
        "category": "Database",
        "keywords": ["amazon aurora", "aurora mysql", "aurora postgresql", "aurora serverless"],
        "feeds": [
            "https://aws.amazon.com/blogs/database/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "DynamoDB",
        "category": "Database",
        "keywords": ["dynamodb", "amazon dynamodb", "dynamo db"],
        "feeds": [
            "https://aws.amazon.com/blogs/database/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "ElastiCache",
        "category": "Database",
        "keywords": ["elasticache", "amazon elasticache", "elasticache for redis", "elasticache for memcached"],
        "feeds": [
            "https://aws.amazon.com/blogs/database/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "MemoryDB for Redis",
        "category": "Database",
        "keywords": ["memorydb", "amazon memorydb", "memorydb for redis"],
        "feeds": [
            "https://aws.amazon.com/blogs/database/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Redshift",
        "category": "Database",
        "keywords": ["amazon redshift", "redshift serverless", "redshift cluster"],
        "feeds": [
            "https://aws.amazon.com/blogs/big-data/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "DocumentDB",
        "category": "Database",
        "keywords": ["amazon documentdb", "documentdb", "document db"],
        "feeds": [
            "https://aws.amazon.com/blogs/database/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Neptune",
        "category": "Database",
        "keywords": ["amazon neptune", "neptune graph", "graph database"],
        "feeds": [
            "https://aws.amazon.com/blogs/database/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Keyspaces (for Apache Cassandra)",
        "category": "Database",
        "keywords": ["amazon keyspaces", "keyspaces", "cassandra"],
        "feeds": [
            "https://aws.amazon.com/blogs/database/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Timestream",
        "category": "Database",
        "keywords": ["amazon timestream", "timestream", "time series database"],
        "feeds": [
            "https://aws.amazon.com/blogs/database/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "QLDB (Quantum Ledger Database)",
        "category": "Database",
        "keywords": ["qldb", "quantum ledger database", "ledger database"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Database Migration Service (DMS)",
        "category": "Database",
        "keywords": ["aws dms", "database migration service", "schema conversion"],
        "feeds": [
            "https://aws.amazon.com/blogs/database/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "RDS on Outposts",
        "category": "Database",
        "keywords": ["rds on outposts"],
        "feeds": [WHATS_NEW_FEED],
    },

    # ── Networking & Content Delivery ────────────────────────────────────────
    {
        "name": "VPC (Virtual Private Cloud)",
        "category": "Networking",
        "keywords": ["amazon vpc", "virtual private cloud", "vpc subnet", "vpc endpoint", "security group", "network acl"],
        "feeds": [
            "https://aws.amazon.com/blogs/networking-and-content-delivery/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "CloudFront",
        "category": "Networking",
        "keywords": ["cloudfront", "amazon cloudfront", "cloudfront distribution", "cloudfront function"],
        "feeds": [
            "https://aws.amazon.com/blogs/networking-and-content-delivery/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Route 53",
        "category": "Networking",
        "keywords": ["route 53", "route53", "amazon route 53", "dns", "hosted zone"],
        "feeds": [
            "https://aws.amazon.com/blogs/networking-and-content-delivery/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "API Gateway",
        "category": "Networking",
        "keywords": ["api gateway", "amazon api gateway", "rest api", "http api", "websocket api"],
        "feeds": [
            "https://aws.amazon.com/blogs/compute/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Elastic Load Balancing",
        "category": "Networking",
        "keywords": ["elastic load balancing", "elb", "application load balancer", "alb", "network load balancer", "nlb", "gateway load balancer"],
        "feeds": [
            "https://aws.amazon.com/blogs/networking-and-content-delivery/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Direct Connect",
        "category": "Networking",
        "keywords": ["aws direct connect", "direct connect gateway"],
        "feeds": [
            "https://aws.amazon.com/blogs/networking-and-content-delivery/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Transit Gateway",
        "category": "Networking",
        "keywords": ["transit gateway", "aws transit gateway", "tgw"],
        "feeds": [
            "https://aws.amazon.com/blogs/networking-and-content-delivery/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Global Accelerator",
        "category": "Networking",
        "keywords": ["aws global accelerator", "global accelerator"],
        "feeds": [
            "https://aws.amazon.com/blogs/networking-and-content-delivery/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "PrivateLink",
        "category": "Networking",
        "keywords": ["aws privatelink", "privatelink", "vpc endpoint service"],
        "feeds": [
            "https://aws.amazon.com/blogs/networking-and-content-delivery/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "VPN (Site-to-Site & Client)",
        "category": "Networking",
        "keywords": ["aws vpn", "site-to-site vpn", "client vpn", "vpn gateway"],
        "feeds": [
            "https://aws.amazon.com/blogs/networking-and-content-delivery/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "App Mesh",
        "category": "Networking",
        "keywords": ["aws app mesh", "app mesh", "service mesh"],
        "feeds": [
            "https://aws.amazon.com/blogs/networking-and-content-delivery/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Cloud Map",
        "category": "Networking",
        "keywords": ["aws cloud map", "cloud map", "service discovery"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Verified Access",
        "category": "Networking",
        "keywords": ["aws verified access", "verified access"],
        "feeds": [
            "https://aws.amazon.com/blogs/networking-and-content-delivery/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "VPC Lattice",
        "category": "Networking",
        "keywords": ["vpc lattice", "amazon vpc lattice"],
        "feeds": [
            "https://aws.amazon.com/blogs/networking-and-content-delivery/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Private 5G",
        "category": "Networking",
        "keywords": ["aws private 5g", "private 5g"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Network Firewall",
        "category": "Networking",
        "keywords": ["aws network firewall", "network firewall"],
        "feeds": [
            "https://aws.amazon.com/blogs/security/feed/",
            WHATS_NEW_FEED,
        ],
    },

    # ── Security, Identity & Compliance ──────────────────────────────────────
    {
        "name": "IAM (Identity & Access Management)",
        "category": "Security",
        "keywords": ["aws iam", "identity and access management", "iam role", "iam policy", "iam user"],
        "feeds": [
            "https://aws.amazon.com/blogs/security/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "IAM Identity Center",
        "category": "Security",
        "keywords": ["iam identity center", "aws sso", "single sign-on", "identity center"],
        "feeds": [
            "https://aws.amazon.com/blogs/security/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Cognito",
        "category": "Security",
        "keywords": ["amazon cognito", "cognito user pool", "cognito identity pool"],
        "feeds": [
            "https://aws.amazon.com/blogs/security/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "KMS (Key Management Service)",
        "category": "Security",
        "keywords": ["aws kms", "key management service", "kms key", "customer managed key"],
        "feeds": [
            "https://aws.amazon.com/blogs/security/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "CloudHSM",
        "category": "Security",
        "keywords": ["cloudhsm", "aws cloudhsm", "hardware security module"],
        "feeds": [
            "https://aws.amazon.com/blogs/security/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Secrets Manager",
        "category": "Security",
        "keywords": ["aws secrets manager", "secrets manager", "secret rotation"],
        "feeds": [
            "https://aws.amazon.com/blogs/security/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Certificate Manager (ACM)",
        "category": "Security",
        "keywords": ["aws certificate manager", "acm", "ssl certificate", "tls certificate"],
        "feeds": [
            "https://aws.amazon.com/blogs/security/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "GuardDuty",
        "category": "Security",
        "keywords": ["amazon guardduty", "guardduty", "threat detection", "malware detection"],
        "feeds": [
            "https://aws.amazon.com/blogs/security/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Inspector",
        "category": "Security",
        "keywords": ["amazon inspector", "aws inspector", "vulnerability assessment"],
        "feeds": [
            "https://aws.amazon.com/blogs/security/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Macie",
        "category": "Security",
        "keywords": ["amazon macie", "macie", "data discovery", "sensitive data"],
        "feeds": [
            "https://aws.amazon.com/blogs/security/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Detective",
        "category": "Security",
        "keywords": ["amazon detective", "aws detective", "security investigation"],
        "feeds": [
            "https://aws.amazon.com/blogs/security/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Security Hub",
        "category": "Security",
        "keywords": ["aws security hub", "security hub", "security findings"],
        "feeds": [
            "https://aws.amazon.com/blogs/security/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Security Lake",
        "category": "Security",
        "keywords": ["amazon security lake", "security lake"],
        "feeds": [
            "https://aws.amazon.com/blogs/security/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "WAF (Web Application Firewall)",
        "category": "Security",
        "keywords": ["aws waf", "web application firewall", "waf rule", "waf acl"],
        "feeds": [
            "https://aws.amazon.com/blogs/security/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Shield",
        "category": "Security",
        "keywords": ["aws shield", "shield advanced", "ddos protection"],
        "feeds": [
            "https://aws.amazon.com/blogs/security/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Firewall Manager",
        "category": "Security",
        "keywords": ["aws firewall manager", "firewall manager"],
        "feeds": [
            "https://aws.amazon.com/blogs/security/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Verified Permissions",
        "category": "Security",
        "keywords": ["amazon verified permissions", "verified permissions", "cedar policy"],
        "feeds": [
            "https://aws.amazon.com/blogs/security/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Directory Service",
        "category": "Security",
        "keywords": ["aws directory service", "aws managed microsoft ad", "active directory"],
        "feeds": [
            "https://aws.amazon.com/blogs/security/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Resource Access Manager (RAM)",
        "category": "Security",
        "keywords": ["aws resource access manager", "aws ram", "resource sharing"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Artifact",
        "category": "Security",
        "keywords": ["aws artifact", "compliance report", "soc report", "pci dss"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Audit Manager",
        "category": "Security",
        "keywords": ["aws audit manager", "audit manager", "compliance audit"],
        "feeds": [
            "https://aws.amazon.com/blogs/security/feed/",
            WHATS_NEW_FEED,
        ],
    },

    # ── Machine Learning & AI ─────────────────────────────────────────────────
    {
        "name": "SageMaker",
        "category": "ML & AI",
        "keywords": ["amazon sagemaker", "sagemaker studio", "sagemaker endpoint", "sagemaker pipeline"],
        "feeds": [
            "https://aws.amazon.com/blogs/machine-learning/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Bedrock",
        "category": "ML & AI",
        "keywords": ["amazon bedrock", "bedrock", "generative ai", "foundation model", "claude", "llama", "titan"],
        "feeds": [
            "https://aws.amazon.com/blogs/machine-learning/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Q (Amazon Q)",
        "category": "ML & AI",
        "keywords": ["amazon q", "amazon q developer", "amazon q business", "amazon q in quicksight"],
        "feeds": [
            "https://aws.amazon.com/blogs/machine-learning/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Rekognition",
        "category": "ML & AI",
        "keywords": ["amazon rekognition", "rekognition", "image recognition", "video analysis", "facial recognition"],
        "feeds": [
            "https://aws.amazon.com/blogs/machine-learning/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Comprehend",
        "category": "ML & AI",
        "keywords": ["amazon comprehend", "comprehend", "natural language processing", "nlp", "text analysis"],
        "feeds": [
            "https://aws.amazon.com/blogs/machine-learning/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Textract",
        "category": "ML & AI",
        "keywords": ["amazon textract", "textract", "document extraction", "ocr"],
        "feeds": [
            "https://aws.amazon.com/blogs/machine-learning/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Transcribe",
        "category": "ML & AI",
        "keywords": ["amazon transcribe", "transcribe", "speech to text", "automatic speech recognition"],
        "feeds": [
            "https://aws.amazon.com/blogs/machine-learning/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Polly",
        "category": "ML & AI",
        "keywords": ["amazon polly", "polly", "text to speech", "neural tts"],
        "feeds": [
            "https://aws.amazon.com/blogs/machine-learning/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Translate",
        "category": "ML & AI",
        "keywords": ["amazon translate", "machine translation", "neural machine translation"],
        "feeds": [
            "https://aws.amazon.com/blogs/machine-learning/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Lex",
        "category": "ML & AI",
        "keywords": ["amazon lex", "lex chatbot", "conversational ai"],
        "feeds": [
            "https://aws.amazon.com/blogs/machine-learning/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Personalize",
        "category": "ML & AI",
        "keywords": ["amazon personalize", "personalize", "recommendation engine"],
        "feeds": [
            "https://aws.amazon.com/blogs/machine-learning/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Forecast",
        "category": "ML & AI",
        "keywords": ["amazon forecast", "time series forecasting"],
        "feeds": [
            "https://aws.amazon.com/blogs/machine-learning/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Fraud Detector",
        "category": "ML & AI",
        "keywords": ["amazon fraud detector", "fraud detector", "fraud detection"],
        "feeds": [
            "https://aws.amazon.com/blogs/machine-learning/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Kendra",
        "category": "ML & AI",
        "keywords": ["amazon kendra", "kendra", "intelligent search", "enterprise search"],
        "feeds": [
            "https://aws.amazon.com/blogs/machine-learning/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "CodeWhisperer / Q Developer",
        "category": "ML & AI",
        "keywords": ["codewhisperer", "amazon codewhisperer", "q developer", "ai code"],
        "feeds": [
            "https://aws.amazon.com/blogs/machine-learning/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Lookout for Equipment",
        "category": "ML & AI",
        "keywords": ["lookout for equipment", "amazon lookout for equipment", "anomaly detection"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Lookout for Vision",
        "category": "ML & AI",
        "keywords": ["lookout for vision", "amazon lookout for vision", "visual inspection"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Lookout for Metrics",
        "category": "ML & AI",
        "keywords": ["lookout for metrics", "amazon lookout for metrics"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Panorama",
        "category": "ML & AI",
        "keywords": ["aws panorama", "panorama appliance", "computer vision edge"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Monitron",
        "category": "ML & AI",
        "keywords": ["amazon monitron", "monitron", "predictive maintenance"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "HealthLake",
        "category": "ML & AI",
        "keywords": ["amazon healthlake", "healthlake", "fhir", "health data"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Augmented AI (A2I)",
        "category": "ML & AI",
        "keywords": ["amazon augmented ai", "a2i", "human review"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "DeepRacer",
        "category": "ML & AI",
        "keywords": ["aws deepracer", "deepracer", "reinforcement learning"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Trainium & Inferentia",
        "category": "ML & AI",
        "keywords": ["trainium", "inferentia", "aws trainium", "aws inferentia", "neuron"],
        "feeds": [
            "https://aws.amazon.com/blogs/machine-learning/feed/",
            WHATS_NEW_FEED,
        ],
    },

    # ── Analytics ────────────────────────────────────────────────────────────
    {
        "name": "Athena",
        "category": "Analytics",
        "keywords": ["amazon athena", "athena", "serverless query"],
        "feeds": [
            "https://aws.amazon.com/blogs/big-data/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "EMR (Elastic MapReduce)",
        "category": "Analytics",
        "keywords": ["amazon emr", "elastic mapreduce", "emr on eks", "hadoop", "spark", "hive"],
        "feeds": [
            "https://aws.amazon.com/blogs/big-data/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Glue",
        "category": "Analytics",
        "keywords": ["aws glue", "glue etl", "glue data catalog", "glue databrew"],
        "feeds": [
            "https://aws.amazon.com/blogs/big-data/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Kinesis",
        "category": "Analytics",
        "keywords": ["amazon kinesis", "kinesis data streams", "kinesis firehose", "kinesis data analytics"],
        "feeds": [
            "https://aws.amazon.com/blogs/big-data/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "MSK (Managed Streaming for Apache Kafka)",
        "category": "Analytics",
        "keywords": ["amazon msk", "managed streaming for apache kafka", "apache kafka", "msk connect"],
        "feeds": [
            "https://aws.amazon.com/blogs/big-data/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "OpenSearch Service",
        "category": "Analytics",
        "keywords": ["amazon opensearch", "opensearch service", "elasticsearch", "opensearch serverless"],
        "feeds": [
            "https://aws.amazon.com/blogs/big-data/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "QuickSight",
        "category": "Analytics",
        "keywords": ["amazon quicksight", "quicksight", "business intelligence", "bi dashboard"],
        "feeds": [
            "https://aws.amazon.com/blogs/big-data/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Data Exchange",
        "category": "Analytics",
        "keywords": ["aws data exchange", "data exchange", "third-party data"],
        "feeds": [
            "https://aws.amazon.com/blogs/big-data/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Lake Formation",
        "category": "Analytics",
        "keywords": ["aws lake formation", "lake formation", "data lake"],
        "feeds": [
            "https://aws.amazon.com/blogs/big-data/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Clean Rooms",
        "category": "Analytics",
        "keywords": ["aws clean rooms", "clean rooms", "collaborative analytics"],
        "feeds": [
            "https://aws.amazon.com/blogs/big-data/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Entity Resolution",
        "category": "Analytics",
        "keywords": ["aws entity resolution", "entity resolution"],
        "feeds": [WHATS_NEW_FEED],
    },

    # ── Application Integration ───────────────────────────────────────────────
    {
        "name": "SQS (Simple Queue Service)",
        "category": "Application Integration",
        "keywords": ["amazon sqs", "simple queue service", "sqs queue", "sqs fifo"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "SNS (Simple Notification Service)",
        "category": "Application Integration",
        "keywords": ["amazon sns", "simple notification service", "sns topic"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "EventBridge",
        "category": "Application Integration",
        "keywords": ["amazon eventbridge", "eventbridge", "event bus", "event rule", "eventbridge pipes"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Step Functions",
        "category": "Application Integration",
        "keywords": ["aws step functions", "step functions", "state machine", "express workflow"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "MQ (Amazon MQ)",
        "category": "Application Integration",
        "keywords": ["amazon mq", "activemq", "rabbitmq"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "AppFlow",
        "category": "Application Integration",
        "keywords": ["amazon appflow", "appflow", "saas integration"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "AppSync",
        "category": "Application Integration",
        "keywords": ["aws appsync", "appsync", "graphql api", "graphql"],
        "feeds": [
            "https://aws.amazon.com/blogs/mobile/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "B2B Data Interchange",
        "category": "Application Integration",
        "keywords": ["aws b2b data interchange", "b2b data interchange", "edi"],
        "feeds": [WHATS_NEW_FEED],
    },

    # ── DevOps & Developer Tools ──────────────────────────────────────────────
    {
        "name": "CodePipeline",
        "category": "DevOps",
        "keywords": ["aws codepipeline", "codepipeline", "ci/cd pipeline", "continuous delivery"],
        "feeds": [
            "https://aws.amazon.com/blogs/devops/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "CodeBuild",
        "category": "DevOps",
        "keywords": ["aws codebuild", "codebuild", "build project"],
        "feeds": [
            "https://aws.amazon.com/blogs/devops/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "CodeDeploy",
        "category": "DevOps",
        "keywords": ["aws codedeploy", "codedeploy", "blue/green deployment"],
        "feeds": [
            "https://aws.amazon.com/blogs/devops/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "CodeCommit",
        "category": "DevOps",
        "keywords": ["aws codecommit", "codecommit", "git repository"],
        "feeds": [
            "https://aws.amazon.com/blogs/devops/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "CodeArtifact",
        "category": "DevOps",
        "keywords": ["aws codeartifact", "codeartifact", "artifact repository", "package repository"],
        "feeds": [
            "https://aws.amazon.com/blogs/devops/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "CloudFormation",
        "category": "DevOps",
        "keywords": ["aws cloudformation", "cloudformation", "cloudformation stack", "infrastructure as code", "cfn"],
        "feeds": [
            "https://aws.amazon.com/blogs/devops/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "CDK (Cloud Development Kit)",
        "category": "DevOps",
        "keywords": ["aws cdk", "cloud development kit", "cdk construct"],
        "feeds": [
            "https://aws.amazon.com/blogs/devops/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Amplify",
        "category": "DevOps",
        "keywords": ["aws amplify", "amplify hosting", "amplify studio", "amplify gen 2"],
        "feeds": [
            "https://aws.amazon.com/blogs/mobile/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Cloud9",
        "category": "DevOps",
        "keywords": ["aws cloud9", "cloud9", "cloud ide"],
        "feeds": [
            "https://aws.amazon.com/blogs/devops/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "CloudShell",
        "category": "DevOps",
        "keywords": ["aws cloudshell", "cloudshell"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Device Farm",
        "category": "DevOps",
        "keywords": ["aws device farm", "device farm", "mobile testing"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "X-Ray",
        "category": "DevOps",
        "keywords": ["aws x-ray", "x-ray", "distributed tracing", "service map"],
        "feeds": [
            "https://aws.amazon.com/blogs/devops/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Fault Injection Service (FIS)",
        "category": "DevOps",
        "keywords": ["aws fis", "fault injection service", "chaos engineering"],
        "feeds": [
            "https://aws.amazon.com/blogs/devops/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "CodeGuru",
        "category": "DevOps",
        "keywords": ["amazon codeguru", "codeguru reviewer", "codeguru profiler"],
        "feeds": [
            "https://aws.amazon.com/blogs/devops/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Corretto",
        "category": "DevOps",
        "keywords": ["amazon corretto", "corretto", "openjdk"],
        "feeds": [WHATS_NEW_FEED],
    },

    # ── Management & Governance ───────────────────────────────────────────────
    {
        "name": "CloudWatch",
        "category": "Management & Governance",
        "keywords": ["amazon cloudwatch", "cloudwatch metrics", "cloudwatch logs", "cloudwatch alarm", "cloudwatch dashboard"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "CloudTrail",
        "category": "Management & Governance",
        "keywords": ["aws cloudtrail", "cloudtrail", "api activity", "audit log"],
        "feeds": [
            "https://aws.amazon.com/blogs/security/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "AWS Config",
        "category": "Management & Governance",
        "keywords": ["aws config", "config rule", "configuration recorder", "conformance pack"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Systems Manager (SSM)",
        "category": "Management & Governance",
        "keywords": ["aws systems manager", "ssm", "parameter store", "session manager", "patch manager", "run command"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Control Tower",
        "category": "Management & Governance",
        "keywords": ["aws control tower", "control tower", "landing zone", "guardrail"],
        "feeds": [
            "https://aws.amazon.com/blogs/aws/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Organizations",
        "category": "Management & Governance",
        "keywords": ["aws organizations", "organizational unit", "scp", "service control policy"],
        "feeds": [
            "https://aws.amazon.com/blogs/security/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Trusted Advisor",
        "category": "Management & Governance",
        "keywords": ["aws trusted advisor", "trusted advisor"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Service Catalog",
        "category": "Management & Governance",
        "keywords": ["aws service catalog", "service catalog", "portfolio", "provisioned product"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "License Manager",
        "category": "Management & Governance",
        "keywords": ["aws license manager", "license manager", "byol"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Well-Architected Tool",
        "category": "Management & Governance",
        "keywords": ["aws well-architected tool", "well-architected", "workload review"],
        "feeds": [
            "https://aws.amazon.com/blogs/architecture/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Health (AWS Health Dashboard)",
        "category": "Management & Governance",
        "keywords": ["aws health", "personal health dashboard", "health event"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Resilience Hub",
        "category": "Management & Governance",
        "keywords": ["aws resilience hub", "resilience hub", "rto", "rpo"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Proton",
        "category": "Management & Governance",
        "keywords": ["aws proton", "proton template", "platform engineering"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "OpsWorks",
        "category": "Management & Governance",
        "keywords": ["aws opsworks", "opsworks", "chef", "puppet"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Chatbot",
        "category": "Management & Governance",
        "keywords": ["aws chatbot", "chatbot slack", "chatbot teams"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Resource Groups & Tag Editor",
        "category": "Management & Governance",
        "keywords": ["resource groups", "tag editor", "aws resource groups"],
        "feeds": [WHATS_NEW_FEED],
    },

    # ── Cost Management ───────────────────────────────────────────────────────
    {
        "name": "Cost Explorer",
        "category": "Cost Management",
        "keywords": ["aws cost explorer", "cost explorer", "cost and usage report"],
        "feeds": [
            "https://aws.amazon.com/blogs/aws-cost-management/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Budgets",
        "category": "Cost Management",
        "keywords": ["aws budgets", "budget alert", "cost budget"],
        "feeds": [
            "https://aws.amazon.com/blogs/aws-cost-management/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Savings Plans & Reserved Instances",
        "category": "Cost Management",
        "keywords": ["savings plans", "reserved instance", "compute savings plan"],
        "feeds": [
            "https://aws.amazon.com/blogs/aws-cost-management/feed/",
            WHATS_NEW_FEED,
        ],
    },

    # ── Migration & Transfer ──────────────────────────────────────────────────
    {
        "name": "Migration Hub",
        "category": "Migration & Transfer",
        "keywords": ["aws migration hub", "migration hub"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Application Migration Service (MGN)",
        "category": "Migration & Transfer",
        "keywords": ["aws application migration service", "cloudendure migration", "aws mgn", "lift and shift"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Application Discovery Service",
        "category": "Migration & Transfer",
        "keywords": ["aws application discovery", "discovery agent", "discovery connector"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "DataSync",
        "category": "Migration & Transfer",
        "keywords": ["aws datasync", "datasync", "data transfer"],
        "feeds": [
            "https://aws.amazon.com/blogs/storage/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Transfer Family",
        "category": "Migration & Transfer",
        "keywords": ["aws transfer family", "transfer family", "sftp", "ftps", "ftp"],
        "feeds": [
            "https://aws.amazon.com/blogs/storage/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Snow Family (Migration)",
        "category": "Migration & Transfer",
        "keywords": ["snowball edge", "snowcone", "snow family migration"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Mainframe Modernization",
        "category": "Migration & Transfer",
        "keywords": ["aws mainframe modernization", "mainframe modernization"],
        "feeds": [WHATS_NEW_FEED],
    },

    # ── Business Applications ─────────────────────────────────────────────────
    {
        "name": "Connect",
        "category": "Business Applications",
        "keywords": ["amazon connect", "contact center", "connect contact flow"],
        "feeds": [
            "https://aws.amazon.com/blogs/contact-center/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "SES (Simple Email Service)",
        "category": "Business Applications",
        "keywords": ["amazon ses", "simple email service", "ses sending"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Pinpoint",
        "category": "Business Applications",
        "keywords": ["amazon pinpoint", "pinpoint", "customer engagement", "push notification"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Chime",
        "category": "Business Applications",
        "keywords": ["amazon chime", "chime sdk", "chime meetings"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "WorkMail",
        "category": "Business Applications",
        "keywords": ["amazon workmail", "workmail"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "WorkDocs",
        "category": "Business Applications",
        "keywords": ["amazon workdocs", "workdocs"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Supply Chain",
        "category": "Business Applications",
        "keywords": ["aws supply chain", "supply chain"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Wickr",
        "category": "Business Applications",
        "keywords": ["aws wickr", "wickr", "secure messaging"],
        "feeds": [WHATS_NEW_FEED],
    },

    # ── End User Computing ────────────────────────────────────────────────────
    {
        "name": "WorkSpaces",
        "category": "End User Computing",
        "keywords": ["amazon workspaces", "workspaces personal", "workspaces thin client"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "AppStream 2.0",
        "category": "End User Computing",
        "keywords": ["amazon appstream", "appstream 2.0", "desktop streaming"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "WorkSpaces Web",
        "category": "End User Computing",
        "keywords": ["amazon workspaces web", "workspaces web", "secure browser"],
        "feeds": [WHATS_NEW_FEED],
    },

    # ── IoT ──────────────────────────────────────────────────────────────────
    {
        "name": "IoT Core",
        "category": "IoT",
        "keywords": ["aws iot core", "iot core", "mqtt", "iot message broker"],
        "feeds": [
            "https://aws.amazon.com/blogs/iot/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "IoT Greengrass",
        "category": "IoT",
        "keywords": ["aws iot greengrass", "greengrass", "iot edge"],
        "feeds": [
            "https://aws.amazon.com/blogs/iot/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "IoT Analytics",
        "category": "IoT",
        "keywords": ["aws iot analytics", "iot analytics"],
        "feeds": [
            "https://aws.amazon.com/blogs/iot/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "IoT Device Management",
        "category": "IoT",
        "keywords": ["aws iot device management", "iot fleet management", "iot device"],
        "feeds": [
            "https://aws.amazon.com/blogs/iot/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "IoT SiteWise",
        "category": "IoT",
        "keywords": ["aws iot sitewise", "sitewise", "industrial iot", "iiot"],
        "feeds": [
            "https://aws.amazon.com/blogs/iot/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "IoT TwinMaker",
        "category": "IoT",
        "keywords": ["aws iot twinmaker", "twinmaker", "digital twin"],
        "feeds": [
            "https://aws.amazon.com/blogs/iot/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "IoT FleetWise",
        "category": "IoT",
        "keywords": ["aws iot fleetwise", "fleetwise", "vehicle data"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "IoT ExpressLink",
        "category": "IoT",
        "keywords": ["aws iot expresslink", "expresslink"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "FreeRTOS",
        "category": "IoT",
        "keywords": ["freertos", "aws freertos", "microcontroller"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "IoT RoboRunner",
        "category": "IoT",
        "keywords": ["aws iot roborunner", "roborunner", "robotics"],
        "feeds": [WHATS_NEW_FEED],
    },

    # ── Media Services ────────────────────────────────────────────────────────
    {
        "name": "Elemental MediaConvert",
        "category": "Media Services",
        "keywords": ["aws elemental mediaconvert", "mediaconvert", "video transcoding"],
        "feeds": [
            "https://aws.amazon.com/blogs/media/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Elemental MediaLive",
        "category": "Media Services",
        "keywords": ["aws elemental medialive", "medialive", "live video encoding"],
        "feeds": [
            "https://aws.amazon.com/blogs/media/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Elemental MediaPackage",
        "category": "Media Services",
        "keywords": ["aws elemental mediapackage", "mediapackage", "video origination"],
        "feeds": [
            "https://aws.amazon.com/blogs/media/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Elemental MediaTailor",
        "category": "Media Services",
        "keywords": ["aws elemental mediatailor", "mediatailor", "ad insertion"],
        "feeds": [
            "https://aws.amazon.com/blogs/media/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Elemental MediaConnect",
        "category": "Media Services",
        "keywords": ["aws elemental mediaconnect", "mediaconnect", "video transport"],
        "feeds": [
            "https://aws.amazon.com/blogs/media/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Interactive Video Service (IVS)",
        "category": "Media Services",
        "keywords": ["amazon ivs", "interactive video service", "live streaming"],
        "feeds": [
            "https://aws.amazon.com/blogs/media/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "Elastic Transcoder",
        "category": "Media Services",
        "keywords": ["amazon elastic transcoder", "elastic transcoder"],
        "feeds": [WHATS_NEW_FEED],
    },
    {
        "name": "Nimble Studio",
        "category": "Media Services",
        "keywords": ["amazon nimble studio", "nimble studio", "content creation"],
        "feeds": [WHATS_NEW_FEED],
    },

    # ── Game Tech ─────────────────────────────────────────────────────────────
    {
        "name": "GameLift",
        "category": "Game Tech",
        "keywords": ["amazon gamelift", "gamelift", "game server", "game hosting"],
        "feeds": [
            "https://aws.amazon.com/blogs/gametech/feed/",
            WHATS_NEW_FEED,
        ],
    },
    {
        "name": "GameSparks",
        "category": "Game Tech",
        "keywords": ["amazon gamesparks", "gamesparks"],
        "feeds": [
            "https://aws.amazon.com/blogs/gametech/feed/",
            WHATS_NEW_FEED,
        ],
    },

    # ── Blockchain ────────────────────────────────────────────────────────────
    {
        "name": "Managed Blockchain",
        "category": "Blockchain",
        "keywords": ["amazon managed blockchain", "managed blockchain", "hyperledger fabric", "ethereum"],
        "feeds": [WHATS_NEW_FEED],
    },

    # ── Quantum Computing ─────────────────────────────────────────────────────
    {
        "name": "Braket",
        "category": "Quantum Computing",
        "keywords": ["amazon braket", "braket", "quantum computing", "quantum algorithm"],
        "feeds": [
            "https://aws.amazon.com/blogs/quantum-computing/feed/",
            WHATS_NEW_FEED,
        ],
    },

    # ── Satellite ─────────────────────────────────────────────────────────────
    {
        "name": "Ground Station",
        "category": "Satellite",
        "keywords": ["aws ground station", "ground station", "satellite data"],
        "feeds": [WHATS_NEW_FEED],
    },

    # ── Robotics ─────────────────────────────────────────────────────────────
    {
        "name": "RoboMaker",
        "category": "Robotics",
        "keywords": ["aws robomaker", "robomaker", "robot operating system", "ros"],
        "feeds": [WHATS_NEW_FEED],
    },

    # ── Architecture & Best Practices ─────────────────────────────────────────
    {
        "name": "Architecture Blog",
        "category": "Architecture",
        "keywords": ["well-architected", "reference architecture", "aws architecture"],
        "feeds": ["https://aws.amazon.com/blogs/architecture/feed/"],
    },
    {
        "name": "AWS Partner Network (APN) Blog",
        "category": "Architecture",
        "keywords": ["aws partner", "apn", "aws marketplace partner"],
        "feeds": ["https://aws.amazon.com/blogs/apn/feed/"],
    },

    # ── Open Source ───────────────────────────────────────────────────────────
    {
        "name": "Open Source Blog",
        "category": "Open Source",
        "keywords": ["open source", "opensource", "aws open source"],
        "feeds": ["https://aws.amazon.com/blogs/opensource/feed/"],
    },
]

# Build a lookup dict by name for fast access
SERVICES_BY_NAME = {s["name"]: s for s in AWS_SERVICES}

# All unique category names, preserving order
CATEGORIES = list(dict.fromkeys(s["category"] for s in AWS_SERVICES))

# Flat list of service names for UI multiselect
SERVICE_NAMES = [s["name"] for s in AWS_SERVICES]
