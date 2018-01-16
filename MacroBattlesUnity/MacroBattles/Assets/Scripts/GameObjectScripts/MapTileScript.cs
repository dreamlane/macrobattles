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
    bottomBarController.bottomBarButton.onClick.AddListener(SelectUnit);
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

    List<TileResourceModel> resources = model.resources;
    if (bottomBarController != null) {
      int resourceType = 0;
      resourceType = GameState.GetResourceTemplate(resources[0].template_key).type;
      bottomBarController.tileCoordsText.text =
          "x:" + model.coordinate_x + " y:" + model.coordinate_y;
      bottomBarController.resourceNameText.text = "";
      bottomBarController.resourceTypeText.text = "" + resourceType;
      bottomBarController.saturationText.text = "" + resources[0].saturation;
      // if unit exists on tile
      if (model.unit_keys.Count != 0) {
        bottomBarController.bottomBarButton.gameObject.SetActive(true);
        bottomBarController.bottomBarButton.GetComponentInChildren<Text>().text = "Select Unit";
      } else {
        bottomBarController.bottomBarButton.gameObject.SetActive(false);
      }
    }

    foreach (TileResourceModel resource in resources) {
      Debug.Log("Resource template key: " + resource.template_key);
      Debug.Log("Resource saturation: " + resource.saturation);
    }
  }

  public void SetModel(MapTileModel model) {
    this.model = model;
  }

  void SelectUnit() {
    Debug.Log ("Unit has been Selected");
    // Update the bottom bar to show unit information.
    bottomBarController.bottomBarButton.gameObject.SetActive(false);
  }
}
