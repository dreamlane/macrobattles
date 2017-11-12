using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class MapTileModel {
  public string key;
  public List<string> resource_keys;
  public int coordinate_x;
  public int coordinate_y;
}

[System.Serializable]
public class MapModel {
  public MapTileModel[] mapTiles;
}
