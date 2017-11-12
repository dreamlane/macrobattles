using System.Collections.Generic;
using UnityEngine;

public class MapEngine : MonoBehaviour {

  private bool mapBuilt = false;

  List<List<GameObject>> mapTiles;
  public MapModel mapModel;

  public GameObject mapTilePrefab;

  void Start() {
    Debug.Log("Start called on MapEngine");
    mapModel = null;
  }

  void Update() {
    if (!mapBuilt) {
      if (mapModel != null) {
        Debug.Log(mapModel);
        buildMap();
      }
    }
  }

  public void setMapModel(MapModel model) {
    mapModel = model;
  }

  private void buildMap() {
    GameObject mapObject = GameObject.FindWithTag("Map");
    foreach (MapTileModel tileModel in mapModel.mapTiles) {
      // Make a new game object for every map tile in the model.
      GameObject tileObject = Instantiate(mapTilePrefab) as GameObject;
      tileObject.transform.parent = mapObject.transform;
      tileObject.transform.localPosition =
          new Vector2(tileModel.coordinate_x, tileModel.coordinate_y);
    }
    mapBuilt = true;
  }

  public bool isMapBuilt() {
    return mapBuilt;
  }
}
