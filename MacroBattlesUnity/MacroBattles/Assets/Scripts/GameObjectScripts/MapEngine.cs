using System.Collections.Generic;
using UnityEngine;

public class MapEngine : MonoBehaviour {

  private bool mapBuilt = false;

  public List<MapTileModel> mapTiles;

  public GameObject mapTilePrefab;
  public GameObject structurePrefab;
  public GameObject unitPrefab;
  public GameObject playerCastlePrefab;
  public GameObject enemyCastlePrefab;

  void Start() {
    Debug.Log("Start called on MapEngine");
    mapTiles = null;
  }

  void Update() {
    if (!mapBuilt) {
      if (mapTiles != null) {
        Debug.Log(mapTiles);
        BuildMap();
      }
    }
  }

  public void SetMapTiles(List<MapTileModel> tiles) {
    mapTiles = tiles;
    // Anytime the tiles are updated, rebuild the map.
    BuildMap();
  }

  private void BuildMap() {
    GameObject mapObject = GameObject.FindWithTag("Map");
    // If the map already has tiles, blow them away and make new ones.
    // TODO: Investigate updating existing tiles, rather than recreating them.
    if (mapObject.transform.childCount > 0) {
      Debug.Log("Destroying maptiles.");
      foreach (Transform child in mapObject.transform) {
        GameObject.Destroy(child.gameObject);
      }
    }

    // Build the game objects for the map.
    foreach (MapTileModel tileModel in mapTiles) {
      // Make a new game object for the map tile.
      GameObject tileObject = Instantiate(mapTilePrefab) as GameObject;
      tileObject.transform.parent = mapObject.transform;
      Renderer renderer = tileObject.GetComponent<Renderer>();
      float x_pos = tileModel.coordinate_x * renderer.bounds.size.x;
      float y_pos = tileModel.coordinate_y * renderer.bounds.size.y;
      float z_pos = PositionConstants.MAP_TILE_Z;
      tileObject.transform.localPosition = new Vector3(x_pos, y_pos, z_pos);
      MapTileScript script = tileObject.GetComponent(typeof(MapTileScript)) as MapTileScript;
      script.x = tileModel.coordinate_x;
      script.y = tileModel.coordinate_y;
      if (tileModel.resources != null) {
        script.SetTileResources(tileModel.resources);
      } else {
        Debug.Log("No resources.");
      }
      // Make a new game object for every unit on the tile.
      // TODO: Make this more interesting for battles that have many units.
      if (tileModel.unit_keys.Count > 0) {
        foreach (string unit_key in tileModel.unit_keys) {
          // TODO: Make this an army marker object, since multiple units land on same tile.
          // TODO: Set up a script that makes the units tappable for information.
          GameObject unitObject = Instantiate(unitPrefab) as GameObject;
          unitObject.transform.parent = tileObject.transform;
          unitObject.transform.localPosition = new Vector3(0, 0, PositionConstants.UNIT_Z);
        }
      }
      // Make a new game object for every structure on the tile.
      if (tileModel.structure_keys.Count > 0) {
        foreach (string structure_key in tileModel.structure_keys) {
          GameObject structureObject = Instantiate(structurePrefab) as GameObject;
          structureObject.transform.parent = tileObject.transform;
          structureObject.transform.localPosition =
              new Vector3(0, 0, PositionConstants.STRUCTURE_Z);
        }
      }
      // Make a new game object for enemy bases.
      if (tileModel.is_enemy_home) {
        GameObject enemyHomeObject = Instantiate(enemyCastlePrefab) as GameObject;
        enemyHomeObject.transform.parent = tileObject.transform;
        enemyHomeObject.transform.localPosition =
            new Vector3(0, 0, PositionConstants.STRUCTURE_Z);
      }
      // Make a new game object for the player base.
      if (tileModel.is_player_home) {
        GameObject playerHomeObject = Instantiate(playerCastlePrefab) as GameObject;
        playerHomeObject.transform.parent = tileObject.transform;
        playerHomeObject.transform.localPosition =
            new Vector3(0, 0, PositionConstants.STRUCTURE_Z);
      }
    }
    mapBuilt = true;
  }

  public bool isMapBuilt() {
    return mapBuilt;
  }
}
