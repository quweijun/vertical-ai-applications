"""
项目配置文件
包含模型配置、领域设置和安全设置
"""

# 模型配置
MODEL_CONFIG = {
    "code_generation": {
        "model_name": "codex",
        "max_length": 1000,
        "temperature": 0.7,
        "max_tokens": 500
    },
    "math_solving": {
        "model_name": "math_solver",
        "max_length": 500,
        "temperature": 0.3,
        "max_tokens": 300
    },
    "medical_qa": {
        "model_name": "medical_advisor",
        "max_length": 800,
        "temperature": 0.5,
        "max_tokens": 400
    },
    "financial_analysis": {
        "model_name": "financial_analyst",
        "max_length": 600,
        "temperature": 0.6,
        "max_tokens": 350
    },
    "education_tutor": {
        "model_name": "education_tutor",
        "max_length": 700,
        "temperature": 0.5,
        "max_tokens": 400
    }
}

# 领域特定设置
DOMAIN_SETTINGS = {
    "medical": {
        "max_symptoms": 5,
        "enable_drug_info": True,
        "require_age": False,
        "emergency_keywords": ["胸痛", "呼吸困难", "昏迷", "大出血"],
        "disclaimer_required": True
    },
    "financial": {
        "max_symbols": 10,
        "enable_real_time": False,
        "risk_warning": True,
        "max_investment_ratio": 0.3,
        "disclaimer_required": True
    },
    "education": {
        "max_questions": 20,
        "enable_progress_tracking": True,
        "allow_solution_display": True,
        "adaptive_learning": False
    },
    "code_generation": {
        "max_code_length": 1000,
        "allow_external_libraries": False,
        "security_scan": True,
        "style_guidelines": "pep8"
    }
}

# 安全设置
SAFETY_SETTINGS = {
    "enable_content_filter": True,
    "require_disclaimer": True,
    "log_unsafe_requests": True,
    "block_harmful_content": True,
    "max_request_length": 5000,
    "rate_limiting": {
        "requests_per_minute": 60,
        "requests_per_hour": 1000
    }
}

# API设置（模拟）
API_SETTINGS = {
    "timeout": 30,
    "retry_attempts": 3,
    "cache_enabled": True,
    "cache_duration": 300  # 5分钟
}

# 日志配置
LOG_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "app.log",
    "max_size": "10MB",
    "backup_count": 5
}