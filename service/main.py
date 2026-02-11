"""
Main module
"""

# TO DO: Remove Hello, World! example
from service.config.bootstrap import initialize_service_resources
from service.config.vocabulary import ResourceName
from service.shared.registry import inject

if __name__ == "__main__":
    try:
        initialize_service_resources()
        logger = inject(ResourceName.LOGGER)
        logger.info("✅ Service initialized successfully")
        print("Hello, World!")
    except Exception as e:
        logger.error(f"❌ Service initialization failed: {e}")
        raise e


# TO DO: Remove this example
def sum_two_numbers(a: int, b: int) -> int:
    """Sum two numbers"""
    return a + b
