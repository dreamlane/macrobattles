using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class MapTileModel {
  public string key;
  public List<TileResourceModel> resources;
  public int coordinate_x;
  public int coordinate_y;
  public List<string> unit_keys;
}

[System.Serializable]
public class TileResourceModel {
  public string template_key;
  public int saturation;
}
