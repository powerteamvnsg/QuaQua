# Assets module - Curated Asset Registry (Style-Verified Only)
from .asset_registry import (
    CuratedAssetRegistry, 
    get_registry, 
    resolve_asset, 
    check_assets_available,
    halt_if_missing
)

# Alias for backward compatibility
AssetRegistry = CuratedAssetRegistry

__all__ = [
    'CuratedAssetRegistry',
    'AssetRegistry',  # Alias
    'get_registry', 
    'resolve_asset', 
    'check_assets_available',
    'halt_if_missing'
]
