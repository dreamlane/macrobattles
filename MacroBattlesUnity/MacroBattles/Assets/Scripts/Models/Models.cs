﻿using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class ResponseModel {
  public string status;
  public string error;
  public string data;
}

[System.Serializable]
public class PlayerModel {
  public string key;
  public string username;
}

[System.Serializable]
public class GameModel {
  // The map tiles that make up the world.
  // See MapModels.cs
  public List<MapTileModel> mapTiles;
  // The units in the game.
  // See UnitModels.cs
  public List<UnitModel> units;
  // The resource templates in the game.
  // See ResourceModels.cs
  public List<ResourceTemplateModel> resource_templates;
}

