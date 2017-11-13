using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class MapTileModel {
  public string key;
  public List<TileResourceModel> resources;
  public int coordinate_x;
  public int coordinate_y;
  public List<string> unit_keys;
  public List<string> structure_keys;
  public bool is_enemy_home;
  public bool is_player_home;
}

[System.Serializable]
public class TileResourceModel {
  public string template_key;
  public int saturation;
}
