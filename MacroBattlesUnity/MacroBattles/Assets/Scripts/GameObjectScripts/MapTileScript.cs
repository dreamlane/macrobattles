using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

public class MapTileScript : MonoBehaviour {
  private MapTileModel model;
  private BottomBarController bottomBarController;
  private GameSceneMain gameSceneMain;

  void Start() {
    GameObject bottomBarObject = GameObject.FindWithTag("BottomBar");
    bottomBarController =
        bottomBarObject.GetComponent(typeof(BottomBarController))
        as BottomBarController;
    // bottomBarController.bottomBarButton.onClick.AddListener(SelectUnit);
  }

  void Update() {

  }

  void OnMouseUpAsButton() {
    if (EventSystem.current.IsPointerOverGameObject()) {
      Debug.Log("Pointer is over a UI element, do not handle click.");
      return;
    }

    // When the tile is tapped, show pertinent information in the bottom bar.
    // Start with Units if any are on the tile. TODO
    // TODO: Ally Units.
    // TODO: Enemy Units.
    if (model.is_player_home) {
      SelectHomeBase();
    } else {
      SelectTileResources();
    }
  }

  public void SetModel(MapTileModel model) {
    this.model = model;
  }

  private void SelectUnit() {
    Debug.Log("Unit has been Selected");
    // Update the bottom bar to show unit information.
    // bottomBarController.bottomBarButton.gameObject.SetActive(false);
  }

  private void SelectHomeBase() {
    Debug.Log("Home Base has been Selected");
    // Update the bottom bar to show home base information.
    bottomBarController.ShowTileHomeBase();
  }

  private void SelectTileResources() {
    bottomBarController.ShowTileResources(model.resources);
  }
}
