# Tensor equality and deduplication

Every candidate module was compared using sorted key names, shapes, dtypes, canonical tensor SHA256 and torch.equal. No filename-based equality was used. All 15 full models passed strict loading.

{
  "distinct_by_family": {
    "diagnostic": 5,
    "anatomy": 5,
    "reliability": 5,
    "residual": 15
  },
  "deduplicated_instances": [
    {
      "seed": 123,
      "fold": 0,
      "family": "diagnostic",
      "shared_file": "diagnostic/fold_0_b73bede5dc80.pt",
      "canonical_tensor_sha256": "b73bede5dc8054a2bb3858b1b17d53c2ba6fb9d7fa629b80215966cd9197747a",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 123,
      "fold": 0,
      "family": "anatomy",
      "shared_file": "anatomy/fold_0_802ef43dc0bd.pt",
      "canonical_tensor_sha256": "802ef43dc0bd4ea00341255e941ce5d428c4847bfa5b5faa4e937de823561835",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 123,
      "fold": 0,
      "family": "reliability",
      "shared_file": "reliability/fold_0_60357e219af4.pt",
      "canonical_tensor_sha256": "60357e219af4188af3bcc41b4c492e28c6119dbc5ee5b2761872e2a2b77e2292",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 123,
      "fold": 1,
      "family": "diagnostic",
      "shared_file": "diagnostic/fold_1_3d92b02b7aea.pt",
      "canonical_tensor_sha256": "3d92b02b7aea776dac4ff78ceb57c5e1d9e28413a4b6660c2cc572b372b0a6dd",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 123,
      "fold": 1,
      "family": "anatomy",
      "shared_file": "anatomy/fold_1_933db1691190.pt",
      "canonical_tensor_sha256": "933db1691190f4fd24c84601ed095e68f320e6788d20c98ec782dee66d42a06a",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 123,
      "fold": 1,
      "family": "reliability",
      "shared_file": "reliability/fold_1_80da98941130.pt",
      "canonical_tensor_sha256": "80da98941130e90b7f059da7cd08eabbb510df4bdf5a0661132a554f4cb92e79",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 123,
      "fold": 2,
      "family": "diagnostic",
      "shared_file": "diagnostic/fold_2_baecb3687e79.pt",
      "canonical_tensor_sha256": "baecb3687e797faf3079495fe23a24944b3856ef9857510fd446d7a92ae891db",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 123,
      "fold": 2,
      "family": "anatomy",
      "shared_file": "anatomy/fold_2_6fb458d1aeef.pt",
      "canonical_tensor_sha256": "6fb458d1aeefa6d4298e57c916d7f730e4e432b7cbcc234eef16911b579f6c40",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 123,
      "fold": 2,
      "family": "reliability",
      "shared_file": "reliability/fold_2_5b5a8c9fe403.pt",
      "canonical_tensor_sha256": "5b5a8c9fe403e0174a612292585767f34de0e85e2bbdfd8f487e54788b48841d",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 123,
      "fold": 3,
      "family": "diagnostic",
      "shared_file": "diagnostic/fold_3_8b007083577a.pt",
      "canonical_tensor_sha256": "8b007083577a371dcbbe50d087fc2806a41a96f9089a910346ac0a070f7eea81",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 123,
      "fold": 3,
      "family": "anatomy",
      "shared_file": "anatomy/fold_3_fa03668b6898.pt",
      "canonical_tensor_sha256": "fa03668b689848771466e5f645d94632385c7c71a8cb2570b803273505935725",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 123,
      "fold": 3,
      "family": "reliability",
      "shared_file": "reliability/fold_3_d3bb7426a356.pt",
      "canonical_tensor_sha256": "d3bb7426a356483b9e134f90a7c1a797e03428fa0fb5590e30f75b568b4d2a18",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 123,
      "fold": 4,
      "family": "diagnostic",
      "shared_file": "diagnostic/fold_4_4577de2a8733.pt",
      "canonical_tensor_sha256": "4577de2a87330e6b7c2de14c2f71a45675e094dbfea6da92aeebb5755fc284d7",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 123,
      "fold": 4,
      "family": "anatomy",
      "shared_file": "anatomy/fold_4_d4f1c8285969.pt",
      "canonical_tensor_sha256": "d4f1c8285969c0ddca442c4979cf8e1c79a86b37be6fe698efd73c4e431b7e7d",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 123,
      "fold": 4,
      "family": "reliability",
      "shared_file": "reliability/fold_4_f1475aa90d59.pt",
      "canonical_tensor_sha256": "f1475aa90d5963986a36fa5975188052909c6880d0e6cf79bc55eb5ea0f48ac3",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 456,
      "fold": 0,
      "family": "diagnostic",
      "shared_file": "diagnostic/fold_0_b73bede5dc80.pt",
      "canonical_tensor_sha256": "b73bede5dc8054a2bb3858b1b17d53c2ba6fb9d7fa629b80215966cd9197747a",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 456,
      "fold": 0,
      "family": "anatomy",
      "shared_file": "anatomy/fold_0_802ef43dc0bd.pt",
      "canonical_tensor_sha256": "802ef43dc0bd4ea00341255e941ce5d428c4847bfa5b5faa4e937de823561835",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 456,
      "fold": 0,
      "family": "reliability",
      "shared_file": "reliability/fold_0_60357e219af4.pt",
      "canonical_tensor_sha256": "60357e219af4188af3bcc41b4c492e28c6119dbc5ee5b2761872e2a2b77e2292",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 456,
      "fold": 1,
      "family": "diagnostic",
      "shared_file": "diagnostic/fold_1_3d92b02b7aea.pt",
      "canonical_tensor_sha256": "3d92b02b7aea776dac4ff78ceb57c5e1d9e28413a4b6660c2cc572b372b0a6dd",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 456,
      "fold": 1,
      "family": "anatomy",
      "shared_file": "anatomy/fold_1_933db1691190.pt",
      "canonical_tensor_sha256": "933db1691190f4fd24c84601ed095e68f320e6788d20c98ec782dee66d42a06a",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 456,
      "fold": 1,
      "family": "reliability",
      "shared_file": "reliability/fold_1_80da98941130.pt",
      "canonical_tensor_sha256": "80da98941130e90b7f059da7cd08eabbb510df4bdf5a0661132a554f4cb92e79",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 456,
      "fold": 2,
      "family": "diagnostic",
      "shared_file": "diagnostic/fold_2_baecb3687e79.pt",
      "canonical_tensor_sha256": "baecb3687e797faf3079495fe23a24944b3856ef9857510fd446d7a92ae891db",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 456,
      "fold": 2,
      "family": "anatomy",
      "shared_file": "anatomy/fold_2_6fb458d1aeef.pt",
      "canonical_tensor_sha256": "6fb458d1aeefa6d4298e57c916d7f730e4e432b7cbcc234eef16911b579f6c40",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 456,
      "fold": 2,
      "family": "reliability",
      "shared_file": "reliability/fold_2_5b5a8c9fe403.pt",
      "canonical_tensor_sha256": "5b5a8c9fe403e0174a612292585767f34de0e85e2bbdfd8f487e54788b48841d",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 456,
      "fold": 3,
      "family": "diagnostic",
      "shared_file": "diagnostic/fold_3_8b007083577a.pt",
      "canonical_tensor_sha256": "8b007083577a371dcbbe50d087fc2806a41a96f9089a910346ac0a070f7eea81",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 456,
      "fold": 3,
      "family": "anatomy",
      "shared_file": "anatomy/fold_3_fa03668b6898.pt",
      "canonical_tensor_sha256": "fa03668b689848771466e5f645d94632385c7c71a8cb2570b803273505935725",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 456,
      "fold": 3,
      "family": "reliability",
      "shared_file": "reliability/fold_3_d3bb7426a356.pt",
      "canonical_tensor_sha256": "d3bb7426a356483b9e134f90a7c1a797e03428fa0fb5590e30f75b568b4d2a18",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 456,
      "fold": 4,
      "family": "diagnostic",
      "shared_file": "diagnostic/fold_4_4577de2a8733.pt",
      "canonical_tensor_sha256": "4577de2a87330e6b7c2de14c2f71a45675e094dbfea6da92aeebb5755fc284d7",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 456,
      "fold": 4,
      "family": "anatomy",
      "shared_file": "anatomy/fold_4_d4f1c8285969.pt",
      "canonical_tensor_sha256": "d4f1c8285969c0ddca442c4979cf8e1c79a86b37be6fe698efd73c4e431b7e7d",
      "equality": "keys/shapes/dtypes/values exact"
    },
    {
      "seed": 456,
      "fold": 4,
      "family": "reliability",
      "shared_file": "reliability/fold_4_f1475aa90d59.pt",
      "canonical_tensor_sha256": "f1475aa90d5963986a36fa5975188052909c6880d0e6cf79bc55eb5ea0f48ac3",
      "equality": "keys/shapes/dtypes/values exact"
    }
  ]
}
