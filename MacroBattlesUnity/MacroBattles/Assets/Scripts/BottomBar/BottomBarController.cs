using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class BottomBarController : MonoBehaviour {

  public Text tileCoordsText;
  // Resource Texts.
  public Text resourceNameText;
  public Text resourceTypeText;
  public Text saturationText;
  public Button bottomBarButton;

  // Unit Texts.
  public Text unitOwnerText;
  public Text healthText;
  public Text orderAvailableText;
  public Text unitTypeText;
  public Text unitNumberText;

	// Use this for initialization
	void Start () {

	}

	// Update is called once per frame
	void Update () {

	}

  void ShowTileResources(List<TileResourceModel> resources) {
    //TODO: implement.
  }

  void ShowTileAllyUnits(List<UnitModel> units) {
    //TODO: implement.
  }

  void ShowTileEnemyUnits(List<UnitModel> units) {
    //TODO: implement.
  }
}
