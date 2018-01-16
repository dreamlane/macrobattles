using System.Collections.Generic;
using System.Linq;
using UnityEngine;

/*
 * The state of the game is primarily just GameModel in a dictionary form.
 * In the future, there may be more data here.
 */
public static class GameState {
  // The map tiles that make up the world.
  // See MapModels.cs
  private static Dictionary<string, MapTileModel> mapTiles;
  // The units in the game.
  // See UnitModels.cs
  private static Dictionary<string, UnitModel> units;
  // The resource templates in the game.
  // See ResourceModels.cs
  private static Dictionary<string, ResourceTemplateModel> resourceTemplates;
  // The equipment in the game.
  // See EquipmentModels.cs
  private static Dictionary<string, EquipmentModel> equipment;
  // The structures in the game.
  // See StructureModels.cs
  private static Dictionary<string, StructureModel> structures;

  public static void UpdateGameModel(GameModel gameModel) {
    ClearGameState();
    // TODO: Dry this up with Generics or something.
    foreach (MapTileModel mapTileModel in gameModel.mapTiles) {
      mapTiles.Add(mapTileModel.key, mapTileModel);
    }
    foreach (UnitModel unitModel in gameModel.units) {
      units.Add(unitModel.key, unitModel);
    }
    foreach (ResourceTemplateModel templateModel in gameModel.resource_templates) {
      resourceTemplates.Add(templateModel.key, templateModel);
    }
    foreach (EquipmentModel equipmentModel in gameModel.equipment) {
      equipment.Add(equipmentModel.key, equipmentModel);
    }
    foreach (StructureModel structuresModel in gameModel.structures) {
      structures.Add(structuresModel.key, structuresModel);
    }
  }

  private static void ClearGameState() {
    mapTiles = new Dictionary<string, MapTileModel>();
    units = new Dictionary<string, UnitModel>();
    resourceTemplates = new Dictionary<string, ResourceTemplateModel>();
    equipment = new Dictionary<string, EquipmentModel>();
    structures = new Dictionary<string, StructureModel>();
  }

  public static bool HasMapTiles() {
    return mapTiles != null && mapTiles.Count > 0;
  }

  public static MapTileModel GetMapTile(string key) {
    if (mapTiles == null) {
      Debug.LogError("GameState.mapTiles is null in GetMapTile call.");
      return null;
    }
    return mapTiles[key];
  }

  public static List<MapTileModel> GetMapTileList() {
    if (mapTiles == null) {
      Debug.LogError("GameState.mapTiles is null in GetMapTileList call.");
      return null;
    }
    return mapTiles.Values.ToList();
  }

  public static UnitModel GetUnit(string key) {
    if (units == null) {
      Debug.LogError("GameState.units is null in GetUnit call.");
      return null;
    }
    return units[key];
  }

  public static ResourceTemplateModel GetResourceTemplate(string key) {
    if (resourceTemplates == null) {
      Debug.LogError("GameState.resourceTemplates is null in GetResourceTemplate call.");
      return null;
    }
    return resourceTemplates[key];
  }

  public static EquipmentModel GetEquipment(string key) {
    if (equipment == null) {
      Debug.LogError("GameState.equipment is null in GetEquipment call.");
      return null;
    }
    return equipment[key];
  }

  public static StructureModel GetStructure(string key) {
    if (structures == null) {
      Debug.LogError("GameState.structures is null in GetStructure call.");
      return null;
    }
    return structures[key];
  }
}
