using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class BottomBarController : MonoBehaviour {

  // Arrow buttons, assigned in the editor.
  public Button leftArrowButton;
  public Button rightArrowButton;

  // Page Number Text, assigned in the editor.
  public Text pageNumberText;

  // Line Texts, assigned in the editor.
  public Text leftLineText1;
  public Text leftLineText2;
  public Text leftLineText3;
  public Text rightLineText1;
  public Text rightLineText2;
  public Text rightLineText3;

  // Action Button, assigned in the editor.
  public Button actionButton;

  // Page Numbers.
  private int currentPage;
  private int totalPages;

  // Arrays of strings for each line of text.
  private Dictionary<string, List<string>> lineStrings;
  private const string LEFT_LINE_1_ID = "LeftLine1";
  private const string LEFT_LINE_2_ID = "LeftLine2";
  private const string LEFT_LINE_3_ID = "LeftLine3";
  private const string RIGHT_LINE_1_ID = "RightLine1";
  private const string RIGHT_LINE_2_ID = "RightLine2";
  private const string RIGHT_LINE_3_ID = "RightLine3";

	// Use this for initialization
	void Start () {
    // Set the page turn button on click listeners.
    leftArrowButton.onClick.AddListener(GotoPreviousPage);
    rightArrowButton.onClick.AddListener(GotoNextPage);

    // TODO: put some placeholder? "Tap on a tile to see some stuff"?
    lineStrings = new Dictionary<string, List<string>>();

    // Hide the action button by default.
    actionButton.gameObject.SetActive(false);
	}

	// Update is called once per frame
	void Update () {

	}

  public void ShowTileResources(List<TileResourceModel> resources) {
    // Hide the action button just incase it was revealed previously.
    actionButton.gameObject.SetActive(false);

    ClearLineStrings();
    totalPages = 0;
    currentPage = 1;

    List<string> resourceTypes = new List<string>();
    List<string> saturations = new List<string>();
    List<string> names = new List<string>();
    List<string> propertyAs = new List<string>();
    List<string> propertyBs = new List<string>();
    List<string> propertyCs = new List<string>();

    foreach (TileResourceModel resource in resources) {
      totalPages += 1;
      ResourceTemplateModel model = GameState.GetResourceTemplate(resource.template_key);
      if (model == null) {
        Debug.LogError("The ResourceTemplateModel was not found on the GameState!");
      }

      // Set the string for the resource type, and its properties.
      // TODO: use constants instead of raw ints here.
      // TODO: use string.Format instead of repeating "Resource Type:".
      string type = "";
      switch (model.type) {
        case 0:
          type = "Metal";
          propertyAs.Add(string.Format("Hardness: {0}", model.metal_properties.hardness));
          propertyBs.Add(string.Format("Lustre: {0}", model.metal_properties.lustre));
          propertyCs.Add(string.Format("Density: {0}", model.metal_properties.density));
          break;
        case 1:
          type = "Wood";
          propertyAs.Add(string.Format("Hardness: {0}", model.wood_properties.hardness));
          propertyBs.Add(string.Format("Workability: {0}", model.wood_properties.workability));
          propertyCs.Add(string.Format("Figure: {0}", model.wood_properties.figure));
          break;
        case 2:
          type = "Leather";
          propertyAs.Add(string.Format("Durability: {0}", model.leather_properties.durability));
          propertyBs.Add(string.Format("Flexibility: {0}", model.leather_properties.flexibility));
          propertyCs.Add(string.Format("Smoothness: {0}", model.leather_properties.smoothness));
          break;
        default:
          Debug.LogError("Some resourceTemplate has a type which is unknown! " + model.type);
          type = "Unknown";
          propertyAs.Add("");
          propertyBs.Add("");
          propertyCs.Add("");
          break;
      }
      resourceTypes.Add("Type: " + type);

      // Set the string for the saturation.
      saturations.Add(string.Format("Saturation: {0}", resource.saturation));

      // Set the string for the name of the resource.
      names.Add("Name: " + model.name);
    }

    // Now all of the strings are setup, so update the UI.
    if (totalPages > 0) {
      lineStrings[LEFT_LINE_1_ID] = resourceTypes;
      lineStrings[LEFT_LINE_2_ID] = saturations;
      lineStrings[LEFT_LINE_3_ID] = names;
      lineStrings[RIGHT_LINE_1_ID] = propertyAs;
      lineStrings[RIGHT_LINE_2_ID] = propertyBs;
      lineStrings[RIGHT_LINE_3_ID] = propertyCs;
      UpdatePage();
    } else {
      Debug.LogError("ShowTileResources ended with totalPages < 1!");
    }
  }

  void ShowTileAllyUnits(List<UnitModel> units) {
    //TODO: implement.
  }

  void ShowTileEnemyUnits(List<UnitModel> units) {
    //TODO: implement.
  }

  public void ShowTileHomeBase() {
    ClearLineStrings();
    currentPage = 1;
    totalPages = 1;

    PlayerModel player = GameState.GetCurrentPlayer();
    if (player == null) {
      Debug.LogError("Player is null in ShowTileHomeBase!");
      return;
    }

    List<string> money = new List<string>();
    money.Add(string.Format("Money: {0}", player.money));
    lineStrings[LEFT_LINE_1_ID] = money;

    // Enable the action button, and set it up for hiring units.
    actionButton.GetComponentInChildren<Text>().text = "Hire Unit";
    actionButton.onClick.AddListener(ShowHireUnitUI);
    actionButton.gameObject.SetActive(true);

    UpdatePage();
  }

  void GotoNextPage() {
    if (currentPage < totalPages) {
      currentPage += 1;
    } else {
      currentPage = 1;
    }
    UpdatePage();
  }

  void GotoPreviousPage() {
    if (currentPage > 1) {
      currentPage -= 1;
    } else {
      currentPage = totalPages;
    }
    UpdatePage();
  }

  private void UpdatePage() {
    // Set the page number text.
    pageNumberText.text = string.Format("{0}/{1}", currentPage, totalPages);
    // Set the line text. TODO: figure out how to dry this up maybe.
    foreach (KeyValuePair<string, List<string>> pair in lineStrings) {
      if (pair.Value.Count >= currentPage) {
        // Determine which text to modify, based on the key in the dict.
        Text textObjectToModify = null;
        switch (pair.Key) {
          case LEFT_LINE_1_ID:
            textObjectToModify = leftLineText1;
            break;
          case LEFT_LINE_2_ID:
            textObjectToModify = leftLineText2;
            break;
          case LEFT_LINE_3_ID:
            textObjectToModify = leftLineText3;
            break;
          case RIGHT_LINE_1_ID:
            textObjectToModify = rightLineText1;
            break;
          case RIGHT_LINE_2_ID:
            textObjectToModify = rightLineText2;
            break;
          case RIGHT_LINE_3_ID:
            textObjectToModify = rightLineText3;
            break;
          default:
            Debug.LogError("An unknown key was used in lineString dict!");
            break;
        }
        // It is important to use -1 here because the pages are not 0-indexed, but the list is!
        textObjectToModify.text = pair.Value[currentPage - 1];
      }
    }
  }

  private void ClearLineStrings() {
    lineStrings = new Dictionary<string, List<string>>();
    lineStrings.Add(LEFT_LINE_1_ID, new List<string>() {""});
    lineStrings.Add(LEFT_LINE_2_ID, new List<string>() {""});
    lineStrings.Add(LEFT_LINE_3_ID, new List<string>() {""});
    lineStrings.Add(RIGHT_LINE_1_ID, new List<string>() {""});
    lineStrings.Add(RIGHT_LINE_2_ID, new List<string>() {""});
    lineStrings.Add(RIGHT_LINE_3_ID, new List<string>() {""});
  }

  private void ShowHireUnitUI() {
    // TODO: Make this actually show a dialog UI.
    Debug.Log("Hire Unit UI should show.");
  }
}
