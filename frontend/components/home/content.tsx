"use client";
import React from "react";
import dynamic from "next/dynamic";
import { TableWrapper } from "../table/table";
import { QuickLinkCard } from "./card-quicklink";
import NextLink from "next/link";
import { Link } from "@nextui-org/react";

// Original quick links logos
import { CanvasLogo } from "../logos/canvaslogo";
import { PaperCutLogo } from "../logos/papercutlogo";
import { JstorLogo } from "../logos/jstorlogo";

// Placeholder logos for academic resources
import { LearningLogo } from "../logos/learning-logo";
import { DegreeLogo } from "../logos/degree-logo";
import { ScheduleLogo } from "../logos/schedule-logo";
import { TranscriptLogo } from "../logos/transcript-logo";
import { PlannerLogo } from "../logos/planner-logo";

// Dynamically imported chart (placeholder for statistics)
const Chart = dynamic(
  () => import("../charts/steam").then((mod) => mod.Steam),
  { ssr: false }
);

export const Content = () => (
  <div className="h-full lg:px-6">
    <div className="flex justify-center gap-4 xl:gap-6 pt-3 px-4 lg:px-0 flex-wrap xl:flex-nowrap max-w-[90rem] mx-auto w-full">
      <div className="mt-6 gap-6 flex flex-col w-full">
        {/* Quick Links Section */}
        <div className="flex flex-col gap-2">
          <h3 className="text-xl font-semibold">Quick Links</h3>
          <div className="grid md:grid-cols-3 grid-cols-1 2xl:grid-cols-4 gap-5 justify-center w-full">
            {/* Original Quick Links */}
            <QuickLinkCard
              href="https://canvas.prometheus.osn.wa.gov/login/saml"
              logo={<CanvasLogo />}
              text="Canvas LMS"
            />
            <QuickLinkCard
              href="https://pep.jstor.org/"
              logo={<JstorLogo />}
              text="JSTOR"
            />
            <QuickLinkCard
              href="https://print.ghc.osn.wa.gov/release"
              logo={<PaperCutLogo />}
              text="PaperCut"
            />
            {/* New Placeholder Quick Links */}
            <QuickLinkCard
              href="/degree-plans"
              logo={<DegreeLogo />}
              text="Degree Plans"
            />
            <QuickLinkCard
              href="/transcripts"
              logo={<TranscriptLogo />}
              text="Transcripts"
            />
            <QuickLinkCard
              href="/study-planner"
              logo={<PlannerLogo />}
              text="Study Planner"
            />
          </div>
        </div>

        {/* Statistics Chart */}
        <div className="h-full flex flex-col gap-2">
          <h3 className="text-xl font-semibold">Statistics</h3>
          <div className="w-full bg-default-50 shadow-lg rounded-2xl p-6">
            <Chart />
          </div>
        </div>
      </div>

      {/* Side Section */}
      <div className="mt-4 gap-2 flex flex-col xl:max-w-md w-full">
        <h3 className="text-xl font-semibold">Reentry & Community</h3>
        <div className="flex flex-col justify-center gap-4 flex-wrap md:flex-nowrap">
          {/* Placeholder cards for reentry resources and community news */}
          <div className="bg-default-50  shadow rounded p-4">
            <h4 className="text-lg font-semibold">Reentry Resources</h4>
            <p className="text-sm">
              Information and guidance for a successful reentry.
            </p>
          </div>
          <div className="bg-default-50  shadow rounded p-4">
            <h4 className="text-lg font-semibold">Community News</h4>
            <p className="text-sm">
              Updates and stories from our community.
            </p>
          </div>
        </div>
      </div>
    </div>

    {/* Latest Activity Table */}
    <div className="flex flex-col justify-center w-full py-5 px-4 lg:px-0 max-w-[90rem] mx-auto gap-3">
      <div className="flex flex-wrap justify-between">
        <h3 className="text-center text-xl font-semibold">Recent Activity</h3>
        <Link
          href="/accounts"
          as={NextLink}
          color="primary"
          className="cursor-pointer"
        >
          View All
        </Link>
      </div>
      <TableWrapper />
    </div>
  </div>
);

export default Content;
